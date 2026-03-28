#!/usr/bin/env python3
"""CorridorIQ data pipeline orchestrator.

Usage:
    python -m pipeline.run_pipeline              # CSV + frontend JSON export
    python -m pipeline.run_pipeline --supabase   # CSV + JSON + Supabase load
"""
from __future__ import annotations

import argparse

from pipeline.loaders.csv_exporter import (
    export_corridors,
    export_frontend_json,
    export_ports,
)
from pipeline.processing.corridor_builder import CORRIDOR_DEFINITIONS, PORT_COUNTRY_MAP
from pipeline.processing.feature_builder import (
    build_corridor_features,
    compute_connectivity_scores,
    compute_port_readiness_scores,
    compute_transition_feasibility_scores,
)
from pipeline.sources.oecd import clean_oecd, compute_corridor_emissions_scores
from pipeline.sources.satellite_proxy import (
    compute_nighttime_lights_proxy_scores,
    compute_no2_proxy_scores,
)
from pipeline.sources.wpi import clean_wpi


# Bottleneck diagnosis and recommendation mapping (mirrors backend diagnosis.py logic)
BOTTLENECK_RECOMMENDATIONS: dict[str, str] = {
    "Port Infrastructure Gap": "Prioritize shore power installations, terminal electrification, and LNG bunkering infrastructure at endpoint ports.",
    "Fuel Transition Gap": "Develop clean-fuel storage, bunkering, and terminal handling capacity for corridor operations.",
    "Pollution Exposure Hotspot": "Implement Emission Control Area (ECA) designation along corridor. Deploy real-time emissions monitoring and enforce slow steaming zones near ports.",
    "Cross-Mode Coordination Gap": "Fund shared planning, dispatch, and handoff processes across port, rail, and inland operators.",
    "Monitoring/Readiness Gap": "Deploy satellite-based MRV (Monitoring, Reporting, Verification) systems. Establish corridor-level emissions baselines using Sentinel-5P and AIS data fusion.",
}


def _diagnose(scores: dict) -> tuple[str, str]:
    """Apply rule-based bottleneck diagnosis matching backend diagnosis.py patterns."""
    em = scores["emissions_score"]
    no2 = scores["no2_score"]
    lights = scores["lights_score"]
    strat = scores["strategic_score"]
    feas = scores["feasibility_score"]
    readiness = scores["readiness_score"]

    # 1. Port Infrastructure Gap: high activity but weak port infrastructure
    if lights >= 65 and strat < 55:
        code = "Port Infrastructure Gap"
    # 2. Fuel Transition Gap: high emissions + decent infrastructure = needs clean fuel
    elif em >= 55 and strat >= 70 and feas >= 55:
        code = "Fuel Transition Gap"
    # 3. Pollution Exposure Hotspot: high NO2 + high activity
    elif no2 >= 60 and lights >= 60:
        code = "Pollution Exposure Hotspot"
    # 4. Cross-Mode Coordination Gap: decent activity but low feasibility
    elif lights >= 60 and feas < 45:
        code = "Cross-Mode Coordination Gap"
    # 5. Monitoring/Readiness Gap: low overall readiness or feasibility
    elif readiness < 50 or feas < 35:
        code = "Monitoring/Readiness Gap"
    # 6. Fallback: pick weakest dimension
    else:
        weakest = min(
            [("Port Infrastructure Gap", strat), ("Fuel Transition Gap", em),
             ("Cross-Mode Coordination Gap", feas), ("Pollution Exposure Hotspot", no2)],
            key=lambda x: x[1],
        )
        code = weakest[0]

    return code, BOTTLENECK_RECOMMENDATIONS[code]


def _generate_explanation(corridor: dict, scores: dict, bottleneck: str) -> str:
    """Generate an AI-style explanation paragraph for each corridor."""
    name = corridor["corridor_name"]
    start = corridor["start_port_id"].replace("_", " ").title()
    end = corridor["end_port_id"].replace("_", " ").title()
    readiness = scores["readiness_score"]

    if readiness >= 70:
        readiness_desc = "strong readiness for near-term decarbonization action"
    elif readiness >= 55:
        readiness_desc = "emerging readiness with room for targeted intervention"
    else:
        readiness_desc = "constrained readiness requiring foundational investment before major intervention"

    return (
        f"The {name} corridor between {start} and {end} demonstrates {readiness_desc} "
        f"(readiness score: {readiness}). "
        f"Its current bottleneck is classified as \"{bottleneck}\", "
        f"driven by the corridor's emissions intensity ({scores['emissions_score']}), "
        f"NO2 pressure ({scores['no2_score']}), and logistics activity ({scores['lights_score']}). "
        f"Port strategic importance ({scores['strategic_score']}) and transition feasibility ({scores['feasibility_score']}) "
        f"shape the recommended intervention priority."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="CorridorIQ data pipeline")
    parser.add_argument("--supabase", action="store_true", help="Also load data into Supabase")
    args = parser.parse_args()

    print("=" * 60)
    print("CorridorIQ Data Pipeline")
    print("=" * 60)

    # Step 1: Clean WPI port data
    print("\n[1/7] Cleaning World Port Index data...")
    port_data = clean_wpi()
    print(f"  -> {len(port_data)} ports cleaned")
    for p in port_data:
        print(f"     {p['port_id']}: services={p['services_score']}, strategic={p['strategic_score']}, readiness={p['readiness_score']}")

    # Step 2: Clean OECD emissions data
    print("\n[2/7] Cleaning OECD Maritime CO2 data...")
    country_emissions = clean_oecd()
    print(f"  -> {len(country_emissions)} countries with emissions data")
    for code, val in sorted(country_emissions.items()):
        print(f"     {code}: {val:,.0f} tonnes CO2")

    # Step 3: Compute corridor-level emissions scores
    print("\n[3/7] Computing corridor emissions scores...")
    corridors = CORRIDOR_DEFINITIONS
    emissions_scores = compute_corridor_emissions_scores(country_emissions, corridors)

    # Step 4: Compute satellite proxy scores
    print("\n[4/7] Computing satellite proxy scores (NO2 + nighttime lights)...")
    no2_scores = compute_no2_proxy_scores(country_emissions, port_data, corridors)
    nighttime_scores = compute_nighttime_lights_proxy_scores(port_data, corridors)

    # Step 5: Compute remaining scores
    print("\n[5/7] Computing readiness, connectivity, and feasibility scores...")
    port_readiness_scores = compute_port_readiness_scores(port_data, corridors)
    connectivity_scores = compute_connectivity_scores(port_data, corridors)
    feasibility_scores = compute_transition_feasibility_scores(port_data, country_emissions, corridors)

    # Step 6: Build final features and export backend CSVs
    print("\n[6/7] Building corridor features and exporting backend CSVs...")
    corridor_features = build_corridor_features(
        corridors=corridors,
        port_data=port_data,
        emissions_scores=emissions_scores,
        no2_scores=no2_scores,
        nighttime_scores=nighttime_scores,
        port_readiness_scores=port_readiness_scores,
        connectivity_scores=connectivity_scores,
        feasibility_scores=feasibility_scores,
    )

    corridors_path = export_corridors(corridor_features)
    ports_path = export_ports(port_data)
    print(f"  -> Backend Corridors: {corridors_path}")
    print(f"  -> Backend Ports:     {ports_path}")

    # Step 7: Build frontend JSON output
    print("\n[7/7] Building frontend JSON output...")
    fe_corridor_scores = []
    for c_def, c_feat in zip(corridors, corridor_features):
        cid = c_def["corridor_id"]
        scores = {
            "emissions_score": int(round(float(c_feat["shipping_emissions_score"]))),
            "no2_score": int(round(float(c_feat["no2_score"]))),
            "lights_score": int(round(float(c_feat["night_lights_score"]))),
            "strategic_score": int(round(float(c_feat["port_readiness_score"]))),
            "feasibility_score": int(round(float(c_feat["transition_feasibility_score"]))),
        }
        # Compute readiness as weighted average matching backend scoring.py
        readiness = round(
            scores["emissions_score"] * 0.125
            + scores["no2_score"] * 0.125
            + scores["lights_score"] * 0.20
            + scores["strategic_score"] * 0.20
            + scores["feasibility_score"] * 0.15
            + float(c_feat["connectivity_score"]) * 0.20,
            1,
        )
        scores["readiness_score"] = readiness
        bottleneck, recommendation = _diagnose(scores)
        explanation = _generate_explanation(c_def, scores, bottleneck)

        fe_corridor_scores.append({
            "id": f"score-{cid}",
            "corridor_id": cid,
            **scores,
            "bottleneck": bottleneck,
            "recommendation": recommendation,
            "ai_explanation": explanation,
        })

    fe_dir = export_frontend_json(
        corridor_features, port_data, fe_corridor_scores,
        country_emissions=country_emissions, port_country_map=PORT_COUNTRY_MAP,
    )
    print(f"  -> Frontend JSON: {fe_dir}")

    # Print summary
    print("\n" + "=" * 60)
    print("CORRIDOR SUMMARY")
    print("=" * 60)
    for sc in fe_corridor_scores:
        print(f"\n  {sc['corridor_id']}")
        print(f"    Readiness: {sc['readiness_score']} | Bottleneck: {sc['bottleneck']}")
        print(f"    Emissions={sc['emissions_score']} NO2={sc['no2_score']} Lights={sc['lights_score']} Strategic={sc['strategic_score']} Feasibility={sc['feasibility_score']}")

    # Optional: Supabase load
    if args.supabase:
        print("\n[Supabase] Loading data into Supabase...")
        from pipeline.loaders.supabase_loader import (
            load_corridor_scores as sb_load_scores,
            load_corridors as sb_load_corridors,
            load_ports as sb_load_ports,
        )

        n_ports = sb_load_ports(port_data)
        print(f"  -> {n_ports} ports loaded")
        n_corridors = sb_load_corridors(corridor_features)
        print(f"  -> {n_corridors} corridors loaded")
        n_scores = sb_load_scores(fe_corridor_scores)
        print(f"  -> {n_scores} corridor scores loaded")

    print("\nDone.")


if __name__ == "__main__":
    main()
