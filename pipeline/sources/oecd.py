"""Clean OECD Maritime Transport CO2 emissions data."""
from __future__ import annotations

import csv
from pathlib import Path

from pipeline.config import RAW_DATA_DIR
from pipeline.processing.normalize import min_max_normalize

# Country codes for our corridor endpoints
CORRIDOR_COUNTRIES = {"SGP", "NLD", "CHN", "USA", "ARE", "IND", "BRA", "KOR", "ESP"}

# International voyage types that represent trade corridor emissions
INTERNATIONAL_SOURCES = {
    "RES_INT_TO",       # International arriving, operated by residents
    "RES_INT_FROM",     # International departing, operated by residents
    "NRES_INT_FROM",    # International departing, operated by non-residents
}


def _find_latest_year(raw_path: Path) -> str:
    """Find the latest annual period in the dataset."""
    years: set[str] = set()
    with open(raw_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tp = row.get("TIME_PERIOD", "")
            if len(tp) == 4 and tp.isdigit():
                years.add(tp)
    return max(years) if years else "2024"


def clean_oecd(raw_path: Path | None = None) -> dict[str, float]:
    """Clean OECD data and return country -> total international emissions (tonnes CO2).

    Returns a dict mapping ISO3 country code to total international maritime CO2 emissions.
    """
    if raw_path is None:
        raw_path = RAW_DATA_DIR / "oecd_maritime_co2.csv"

    latest_year = _find_latest_year(raw_path)
    country_emissions: dict[str, float] = {}

    with open(raw_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ref_area = row.get("REF_AREA", "")
            if ref_area not in CORRIDOR_COUNTRIES:
                continue
            if row.get("MEASURE") != "EMISSIONS":
                continue
            if row.get("VESSEL") != "ALL_VESSELS":
                continue
            if row.get("METHODOLOGY") != "_Z":
                continue
            tp = row.get("TIME_PERIOD", "")
            if tp != latest_year:
                continue
            source = row.get("VESSEL_EMISSIONS_SOURCE", "")
            if source not in INTERNATIONAL_SOURCES:
                continue
            obs = row.get("OBS_VALUE", "")
            if not obs:
                continue
            try:
                val = float(obs)
            except ValueError:
                continue
            country_emissions[ref_area] = country_emissions.get(ref_area, 0.0) + val

    return country_emissions


def compute_corridor_emissions_scores(
    country_emissions: dict[str, float],
    corridors: list[dict],
) -> dict[str, float]:
    """Compute shipping_emissions_score (0-100) for each corridor.

    Each corridor has a start_country_code and end_country_code.
    Score = average of both endpoint emissions, then min-max normalized.
    """
    corridor_ids = [c["corridor_id"] for c in corridors]
    raw_scores: list[float] = []

    for corridor in corridors:
        start_code = corridor["start_country_code"]
        end_code = corridor["end_country_code"]
        start_em = country_emissions.get(start_code, 0.0)
        end_em = country_emissions.get(end_code, 0.0)
        raw_scores.append((start_em + end_em) / 2.0)

    normalized = min_max_normalize(raw_scores)
    return dict(zip(corridor_ids, normalized))
