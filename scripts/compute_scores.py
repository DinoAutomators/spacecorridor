"""
Combine all processed data sources → compute corridor readiness scores.

Reads: ports.json, corridors.json, no2_stats.json, viirs_stats.json, oecd_emissions.json
Outputs: corridor_scores.json (with readiness scores, bottlenecks, recommendations, AI explanations)

Scoring weights:
  - Emissions: 25%
  - NO2: 20%
  - Lights: 20%
  - Strategic: 20%
  - Feasibility: 15%
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

WEIGHTS = {
    "emissions": 0.25,
    "no2": 0.20,
    "lights": 0.20,
    "strategic": 0.20,
    "feasibility": 0.15,
}

BOTTLENECK_MAP = {
    "emissions_score": "Fuel Transition Gap",
    "no2_score": "Pollution Exposure Hotspot",
    "lights_score": "Monitoring/Readiness Gap",
    "strategic_score": "Cross-Mode Coordination Gap",
    "feasibility_score": "Port Infrastructure Gap",
}

RECOMMENDATION_MAP = {
    "Port Infrastructure Gap": (
        "Prioritize shore power installations and LNG bunkering infrastructure "
        "at endpoint ports. Consider public-private partnerships for green port upgrades."
    ),
    "Fuel Transition Gap": (
        "Accelerate alternative fuel adoption through methanol/ammonia bunkering pilots. "
        "Establish green fuel corridors with bilateral agreements between port states."
    ),
    "Pollution Exposure Hotspot": (
        "Implement Emission Control Area (ECA) designation along corridor. "
        "Deploy real-time emissions monitoring and enforce slow steaming zones near ports."
    ),
    "Cross-Mode Coordination Gap": (
        "Develop intermodal digital freight platforms connecting maritime, rail, and road. "
        "Align customs procedures for seamless green corridor certification."
    ),
    "Monitoring/Readiness Gap": (
        "Deploy satellite-based MRV (Monitoring, Reporting, Verification) systems. "
        "Establish corridor-level emissions baselines using Sentinel-5P and AIS data fusion."
    ),
}


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def normalize_no2(ports: list) -> dict:
    """Convert raw NO2 values to 0-100 score (lower NO2 = higher score)."""
    no2_values = {p["id"]: p["no2_mean"] for p in ports}
    max_no2 = max(no2_values.values()) or 1
    return {pid: round(100 * (1 - val / max_no2)) for pid, val in no2_values.items()}


def normalize_viirs(ports: list) -> dict:
    """Convert VIIRS radiance to 0-100 score (higher activity = higher score)."""
    viirs_values = {p["id"]: p["viirs_mean"] for p in ports}
    max_viirs = max(viirs_values.values()) or 1
    return {pid: round(100 * val / max_viirs) for pid, val in viirs_values.items()}


def generate_explanation(corridor: dict, scores: dict, ports: dict, bottleneck: str) -> str:
    """Generate a 3-4 sentence AI explanation for the corridor."""
    from_port = ports[corridor["from_port_id"]]
    to_port = ports[corridor["to_port_id"]]
    readiness = scores["readiness_score"]

    # Build contextual explanation
    if readiness >= 70:
        readiness_text = f"emerges as a high-readiness corridor (score: {readiness})"
    elif readiness >= 50:
        readiness_text = f"shows moderate decarbonization readiness (score: {readiness})"
    else:
        readiness_text = f"faces significant readiness challenges (score: {readiness})"

    no2_context = (
        f"NO2 levels around {from_port['name']} ({from_port['no2_mean']} µmol/m²) "
        f"and {to_port['name']} ({to_port['no2_mean']} µmol/m²)"
    )

    viirs_context = (
        f"VIIRS nighttime radiance ({from_port['viirs_mean']}-{to_port['viirs_mean']} nW/cm²/sr)"
    )

    explanation = (
        f"The {corridor['name']} corridor {readiness_text}, "
        f"reflecting {'both ports\' strong infrastructure' if readiness >= 60 else 'infrastructure and emissions challenges at both endpoints'}. "
        f"{no2_context} {'indicate elevated pollution from maritime traffic' if (from_port['no2_mean'] + to_port['no2_mean']) / 2 > 35 else 'suggest relatively moderate pollution levels'}. "
        f"{viirs_context} {'confirms significant economic activity' if (from_port['viirs_mean'] + to_port['viirs_mean']) / 2 > 30 else 'indicates developing port operational capacity'}. "
        f"The primary bottleneck — {bottleneck} — should be the focus of targeted intervention."
    )

    return explanation


def main():
    ports = load_json("ports.json")
    corridors = load_json("corridors.json")

    if not ports or not corridors:
        print("Missing ports.json or corridors.json — run process_wpi.py first")
        return

    ports_by_id = {p["id"]: p for p in ports}
    no2_scores = normalize_no2(ports)
    viirs_scores = normalize_viirs(ports)

    corridor_scores = []
    for corridor in corridors:
        from_id = corridor["from_port_id"]
        to_id = corridor["to_port_id"]

        # Average port-pair scores
        no2_score = round((no2_scores.get(from_id, 50) + no2_scores.get(to_id, 50)) / 2)
        lights_score = round((viirs_scores.get(from_id, 50) + viirs_scores.get(to_id, 50)) / 2)

        from_port = ports_by_id.get(from_id, {})
        to_port = ports_by_id.get(to_id, {})

        strategic_score = round(
            (from_port.get("strategic_score", 50) + to_port.get("strategic_score", 50)) / 2
        )
        feasibility_score = round(
            (from_port.get("services_score", 50) + to_port.get("services_score", 50)) / 2
        )

        # Emissions score (from OECD if available, otherwise estimate from NO2 correlation)
        oecd_data = load_json("oecd_emissions.json")
        if oecd_data and corridor["id"] in oecd_data:
            emissions_score = oecd_data[corridor["id"]].get("emissions_score", 50)
        else:
            # Estimate: inverse of average NO2 with some noise
            emissions_score = max(20, min(80, 100 - round(
                (from_port.get("no2_mean", 30) + to_port.get("no2_mean", 30)) / 1.2
            )))

        # Compute readiness
        readiness_score = round(
            emissions_score * WEIGHTS["emissions"]
            + no2_score * WEIGHTS["no2"]
            + lights_score * WEIGHTS["lights"]
            + strategic_score * WEIGHTS["strategic"]
            + feasibility_score * WEIGHTS["feasibility"]
        )

        # Classify bottleneck
        score_map = {
            "emissions_score": emissions_score,
            "no2_score": no2_score,
            "lights_score": lights_score,
            "strategic_score": strategic_score,
            "feasibility_score": feasibility_score,
        }
        lowest_key = min(score_map, key=score_map.get)
        bottleneck = BOTTLENECK_MAP[lowest_key]
        recommendation = RECOMMENDATION_MAP[bottleneck]

        scores = {
            "emissions_score": emissions_score,
            "no2_score": no2_score,
            "lights_score": lights_score,
            "strategic_score": strategic_score,
            "feasibility_score": feasibility_score,
            "readiness_score": readiness_score,
        }

        explanation = generate_explanation(corridor, scores, ports_by_id, bottleneck)

        corridor_scores.append({
            "id": f"score-{corridor['id']}",
            "corridor_id": corridor["id"],
            **scores,
            "bottleneck": bottleneck,
            "recommendation": recommendation,
            "ai_explanation": explanation,
        })

        print(
            f"  {corridor['name']}: readiness={readiness_score}, bottleneck={bottleneck}"
        )

    out_path = os.path.join(DATA_DIR, "corridor_scores.json")
    with open(out_path, "w") as f:
        json.dump(corridor_scores, f, indent=2)

    print(f"\nWrote {len(corridor_scores)} corridor scores to {out_path}")


if __name__ == "__main__":
    main()
