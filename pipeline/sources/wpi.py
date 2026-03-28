"""Clean World Port Index data and produce PortRecord-compatible rows."""
from __future__ import annotations

import csv
from pathlib import Path

from pipeline.config import RAW_DATA_DIR

# WPI index numbers for corridor ports — IDs match frontend convention
TARGET_PORTS: dict[str, dict] = {
    # Original 10
    "50000.0": {"port_id": "singapore", "port_name": "Singapore", "country": "Singapore", "region": "Southeast Asia"},
    "31140.0": {"port_id": "rotterdam", "port_name": "Rotterdam", "country": "Netherlands", "region": "Western Europe"},
    "59970.0": {"port_id": "shanghai", "port_name": "Shanghai", "country": "China", "region": "East Asia"},
    "16080.0": {"port_id": "los_angeles", "port_name": "Los Angeles", "country": "United States", "region": "North America"},
    "48276.0": {"port_id": "jebel_ali", "port_name": "Jebel Ali", "country": "United Arab Emirates", "region": "Middle East"},
    "48840.0": {"port_id": "mumbai", "port_name": "Mumbai (JNPT)", "country": "India", "region": "South Asia"},
    "12970.0": {"port_id": "santos", "port_name": "Santos", "country": "Brazil", "region": "South America"},
    "60390.0": {"port_id": "busan", "port_name": "Busan", "country": "South Korea", "region": "East Asia"},
    "16070.0": {"port_id": "long_beach", "port_name": "Long Beach", "country": "United States", "region": "North America"},
    "38310.0": {"port_id": "algeciras", "port_name": "Algeciras", "country": "Spain", "region": "Southern Europe"},
    # New ports for 20 corridors
    "61390.0": {"port_id": "yokohama", "port_name": "Yokohama", "country": "Japan", "region": "East Asia"},
    "54030.0": {"port_id": "melbourne", "port_name": "Melbourne", "country": "Australia", "region": "Oceania"},
    "49930.0": {"port_id": "port_klang", "port_name": "Port Klang", "country": "Malaysia", "region": "Southeast Asia"},
    "57840.0": {"port_id": "hong_kong", "port_name": "Hong Kong", "country": "Hong Kong", "region": "East Asia"},
    "30780.0": {"port_id": "hamburg", "port_name": "Hamburg", "country": "Germany", "region": "Northern Europe"},
    "35580.0": {"port_id": "southampton", "port_name": "Southampton", "country": "United Kingdom", "region": "Northern Europe"},
    "35840.0": {"port_id": "le_havre", "port_name": "Le Havre", "country": "France", "region": "Western Europe"},
    "18150.0": {"port_id": "vancouver", "port_name": "Vancouver", "country": "Canada", "region": "North America"},
    "43420.0": {"port_id": "istanbul", "port_name": "Istanbul", "country": "Turkey", "region": "Eastern Mediterranean"},
    "46850.0": {"port_id": "durban", "port_name": "Durban", "country": "South Africa", "region": "Southern Africa"},
    "42230.0": {"port_id": "piraeus", "port_name": "Piraeus", "country": "Greece", "region": "Eastern Mediterranean"},
    "57920.0": {"port_id": "kaohsiung", "port_name": "Kaohsiung", "country": "Taiwan", "region": "East Asia"},
    "57680.0": {"port_id": "hai_phong", "port_name": "Hai Phong", "country": "Vietnam", "region": "Southeast Asia"},
    "57462.0": {"port_id": "laem_chabang", "port_name": "Laem Chabang", "country": "Thailand", "region": "Southeast Asia"},
    "49240.0": {"port_id": "colombo", "port_name": "Colombo", "country": "Sri Lanka", "region": "South Asia"},
    "48140.0": {"port_id": "jeddah", "port_name": "Jeddah", "country": "Saudi Arabia", "region": "Middle East"},
    "9240.0":  {"port_id": "houston", "port_name": "Houston", "country": "United States", "region": "North America"},
    "45165.0": {"port_id": "alexandria", "port_name": "Alexandria", "country": "Egypt", "region": "Eastern Mediterranean"},
    "51587.0": {"port_id": "tanjung_pelepas", "port_name": "Tanjung Pelepas", "country": "Malaysia", "region": "Southeast Asia"},
}

HARBOR_SIZE_SCORE = {"Large": 90, "Medium": 70, "Small": 50, "Very Small": 30}
DEPTH_THRESHOLDS = [(15.0, 20), (12.0, 15), (9.0, 10), (6.0, 5)]
DRY_DOCK_SCORE = {"Large": 15, "Medium": 10, "Small": 5}
YES_VALUES = {"Yes", "yes", "Y", "y"}


def _parse_float(value: str | None) -> float:
    if not value:
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def _bool_flag(value: str | None) -> bool:
    return value in YES_VALUES if value else False


def _compute_services_score(row: dict) -> float:
    flags = [
        ("Services - Electricity", 15),
        ("Services - Longshoremen", 10),
        ("Services - Navigation Equipment", 10),
        ("Supplies - Fuel Oil", 10),
        ("Supplies - Diesel Oil", 10),
        ("Repairs", 15),
        ("Dry Dock", 10),
        ("Communications - Rail", 10),
        ("Communications - Airport", 10),
    ]
    score = 0.0
    for col, weight in flags:
        val = row.get(col, "")
        if col == "Repairs":
            if val == "Major":
                score += weight
            elif val in ("Moderate", "Limited"):
                score += weight * 0.5
        elif col == "Dry Dock":
            score += DRY_DOCK_SCORE.get(val, 0) * weight / 15
        elif _bool_flag(val):
            score += weight
    return min(100.0, score)


def _compute_strategic_score(row: dict) -> float:
    harbor_size = row.get("Harbor Size", "")
    base = HARBOR_SIZE_SCORE.get(harbor_size, 30)
    cargo_depth = _parse_float(row.get("Cargo Pier Depth (m)"))
    depth_bonus = 0
    for threshold, bonus in [(15.0, 20), (12.0, 15), (9.0, 10), (6.0, 5)]:
        if cargo_depth >= threshold:
            depth_bonus = bonus
            break
    return min(100.0, float(base + depth_bonus))


def _compute_readiness_score(row: dict) -> float:
    score = 0.0
    if _bool_flag(row.get("Services - Electricity")):
        score += 25
    if row.get("Dry Dock") in ("Large", "Medium"):
        score += 15
    if _bool_flag(row.get("Communications - Rail")) or row.get("Railway") in ("Large", "Medium", "Small"):
        score += 15
    shelter = row.get("Shelter Afforded", "")
    if shelter == "Excellent":
        score += 15
    elif shelter == "Good":
        score += 10
    elif shelter == "Fair":
        score += 5
    cargo_depth = _parse_float(row.get("Cargo Pier Depth (m)"))
    if cargo_depth >= 15:
        score += 15
    elif cargo_depth >= 10:
        score += 10
    elif cargo_depth >= 6:
        score += 5
    if _bool_flag(row.get("Supplies - Fuel Oil")) and _bool_flag(row.get("Supplies - Diesel Oil")):
        score += 10
    if row.get("Repairs") == "Major":
        score += 5
    return min(100.0, score)


def clean_wpi(raw_path: Path | None = None) -> list[dict]:
    if raw_path is None:
        raw_path = RAW_DATA_DIR / "wpi_ports.csv"

    ports: list[dict] = []
    with open(raw_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            wpi_num = row.get("World Port Index Number", "")
            if wpi_num not in TARGET_PORTS:
                continue
            meta = TARGET_PORTS[wpi_num]
            lat = _parse_float(row.get("Latitude"))
            lon = _parse_float(row.get("Longitude"))
            if lat == 0.0 and lon == 0.0:
                continue

            ports.append({
                "port_id": meta["port_id"],
                "port_name": meta["port_name"],
                "country": meta["country"],
                "region": meta["region"],
                "mode": "port",
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "harbor_type": row.get("Harbor Type", ""),
                "cargo_capability": "true",
                "services_score": round(_compute_services_score(row), 2),
                "strategic_score": round(_compute_strategic_score(row), 2),
                "readiness_score": round(_compute_readiness_score(row), 2),
            })

    return sorted(ports, key=lambda p: p["port_id"])
