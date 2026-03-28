"""Derive NO2 and nighttime lights proxy scores without GEE access.

NO2 proxy: derived from OECD country emissions (higher emissions = higher atmospheric NO2 proxy).
Nighttime lights proxy: derived from WPI port strategic score + emissions volume (busy ports = more activity).

Both scores are documented as proxy-based approximations.
"""
from __future__ import annotations

from pipeline.processing.normalize import min_max_normalize


def compute_no2_proxy_scores(
    country_emissions: dict[str, float],
    port_data: list[dict],
    corridors: list[dict],
) -> dict[str, float]:
    """Compute no2_score (0-100) as a proxy from OECD emissions + port activity.

    Combines country-level emissions (70%) with port strategic importance (30%)
    so the NO2 proxy reflects both atmospheric load and local port intensity.
    """
    port_lookup = {p["port_id"]: p for p in port_data}
    raw_scores: list[float] = []
    for corridor in corridors:
        start_em = country_emissions.get(corridor["start_country_code"], 0.0)
        end_em = country_emissions.get(corridor["end_country_code"], 0.0)
        emissions_component = (start_em + end_em) / 2.0

        start_port = port_lookup.get(corridor["start_port_id"], {})
        end_port = port_lookup.get(corridor["end_port_id"], {})
        port_component = (
            float(start_port.get("strategic_score", 50))
            + float(end_port.get("strategic_score", 50))
        ) / 2.0

        # Weight emissions 70%, port importance 30% (scale port to same magnitude)
        max_em = max(country_emissions.values()) if country_emissions else 1.0
        raw_scores.append(emissions_component / max_em * 70.0 + port_component / 100.0 * 30.0)

    normalized = min_max_normalize(raw_scores)
    return dict(zip([c["corridor_id"] for c in corridors], normalized))


def compute_nighttime_lights_proxy_scores(
    port_data: list[dict],
    corridors: list[dict],
) -> dict[str, float]:
    """Compute night_lights_score (0-100) as a proxy from port activity indicators.

    Combines strategic_score and services_score from WPI as a logistics activity proxy.
    """
    port_lookup = {p["port_id"]: p for p in port_data}
    raw_scores: list[float] = []

    for corridor in corridors:
        start_port = port_lookup.get(corridor["start_port_id"], {})
        end_port = port_lookup.get(corridor["end_port_id"], {})

        start_activity = (
            float(start_port.get("strategic_score", 50))
            + float(start_port.get("services_score", 50))
        ) / 2.0
        end_activity = (
            float(end_port.get("strategic_score", 50))
            + float(end_port.get("services_score", 50))
        ) / 2.0
        raw_scores.append((start_activity + end_activity) / 2.0)

    normalized = min_max_normalize(raw_scores)
    return dict(zip([c["corridor_id"] for c in corridors], normalized))
