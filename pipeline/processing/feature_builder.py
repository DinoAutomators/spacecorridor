"""Compose the 6 corridor scores from cleaned data sources."""
from __future__ import annotations

import json

from pipeline.processing.normalize import min_max_normalize


def _avg_port_field(
    port_data: list[dict],
    start_port_id: str,
    end_port_id: str,
    field: str,
    default: float = 50.0,
) -> float:
    port_lookup = {p["port_id"]: p for p in port_data}
    start = float(port_lookup.get(start_port_id, {}).get(field, default))
    end = float(port_lookup.get(end_port_id, {}).get(field, default))
    return (start + end) / 2.0


def compute_port_readiness_scores(
    port_data: list[dict],
    corridors: list[dict],
) -> dict[str, float]:
    """port_readiness_score = avg of endpoint ports' readiness_score."""
    raw = []
    for c in corridors:
        raw.append(_avg_port_field(port_data, c["start_port_id"], c["end_port_id"], "readiness_score"))
    normalized = min_max_normalize(raw)
    return dict(zip([c["corridor_id"] for c in corridors], normalized))


def compute_connectivity_scores(
    port_data: list[dict],
    corridors: list[dict],
) -> dict[str, float]:
    """connectivity_score = proxy from port railway access + services.

    Uses a composite of services_score and railway/rail indicators.
    """
    port_lookup = {p["port_id"]: p for p in port_data}
    raw = []
    for c in corridors:
        start = port_lookup.get(c["start_port_id"], {})
        end = port_lookup.get(c["end_port_id"], {})
        start_conn = float(start.get("services_score", 50))
        end_conn = float(end.get("services_score", 50))
        raw.append((start_conn + end_conn) / 2.0)
    normalized = min_max_normalize(raw)
    return dict(zip([c["corridor_id"] for c in corridors], normalized))


def compute_transition_feasibility_scores(
    port_data: list[dict],
    country_emissions: dict[str, float],
    corridors: list[dict],
) -> dict[str, float]:
    """transition_feasibility_score = composite of port infrastructure + emissions leverage.

    Higher port readiness + strategic importance + moderate emissions = higher feasibility.
    """
    port_lookup = {p["port_id"]: p for p in port_data}
    raw = []
    for c in corridors:
        start = port_lookup.get(c["start_port_id"], {})
        end = port_lookup.get(c["end_port_id"], {})

        # Infrastructure readiness component (60%)
        infra = (
            float(start.get("readiness_score", 50))
            + float(end.get("readiness_score", 50))
            + float(start.get("strategic_score", 50))
            + float(end.get("strategic_score", 50))
        ) / 4.0

        # Emissions leverage: moderate emissions are more feasible than extreme
        start_em = country_emissions.get(c["start_country_code"], 0.0)
        end_em = country_emissions.get(c["end_country_code"], 0.0)
        avg_em = (start_em + end_em) / 2.0
        raw.append(infra * 0.6 + avg_em * 0.4)

    normalized = min_max_normalize(raw)
    return dict(zip([c["corridor_id"] for c in corridors], normalized))


def build_corridor_features(
    corridors: list[dict],
    port_data: list[dict],
    emissions_scores: dict[str, float],
    no2_scores: dict[str, float],
    nighttime_scores: dict[str, float],
    port_readiness_scores: dict[str, float],
    connectivity_scores: dict[str, float],
    feasibility_scores: dict[str, float],
) -> list[dict]:
    """Compose final corridor_features rows matching the data_dictionary.md contract."""
    rows = []
    for c in corridors:
        cid = c["corridor_id"]
        rows.append({
            "corridor_id": cid,
            "corridor_name": c["corridor_name"],
            "start_port": c["start_port_id"],
            "end_port": c["end_port_id"],
            "region": c["region"],
            "mode": c["mode"],
            "time_period": c["time_period"],
            "description": c["description"],
            "strategic_importance_note": c["strategic_importance_note"],
            "geometry": json.dumps(c["geometry"]) if isinstance(c["geometry"], (dict, list)) else str(c["geometry"]),
            "no2_score": round(no2_scores.get(cid, 50.0), 2),
            "night_lights_score": round(nighttime_scores.get(cid, 50.0), 2),
            "shipping_emissions_score": round(emissions_scores.get(cid, 50.0), 2),
            "port_readiness_score": round(port_readiness_scores.get(cid, 50.0), 2),
            "connectivity_score": round(connectivity_scores.get(cid, 50.0), 2),
            "transition_feasibility_score": round(feasibility_scores.get(cid, 50.0), 2),
        })
    return rows
