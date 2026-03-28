"""
Parse World Port Index (WPI) CSV → filtered ports JSON for SpaceCorridor.

Input:  data/raw/UpdatedPub150.csv
Output: data/processed/ports.json

Target ports: Singapore, Rotterdam, Shanghai, Los Angeles, Jebel Ali,
              Mumbai (JNPT), Busan, Long Beach, Algeciras, Santos
"""

import json
import os
import pandas as pd

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "UpdatedPub150.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "ports.json")

# Map WPI port names to our IDs
TARGET_PORTS = {
    "SINGAPORE": "singapore",
    "ROTTERDAM": "rotterdam",
    "SHANGHAI": "shanghai",
    "LOS ANGELES": "los_angeles",
    "JABAL ALI": "jebel_ali",  # WPI uses JABAL ALI
    "MUMBAI": "mumbai",
    "BUSAN": "busan",
    "LONG BEACH": "long_beach",
    "ALGECIRAS": "algeciras",
    "SANTOS": "santos",
}

HARBOR_SIZE_MAP = {"L": 3, "M": 2, "S": 1, "V": 0}
SHELTER_MAP = {"E": 3, "G": 2, "F": 1, "P": 0, "N": 0}


def derive_services_score(row: pd.Series) -> int:
    """Derive a 0-100 services score from WPI facility fields."""
    score = 0
    # Harbor size (0-30)
    score += HARBOR_SIZE_MAP.get(str(row.get("Harbor Size", "S")), 1) * 10
    # Shelter (0-20)
    score += SHELTER_MAP.get(str(row.get("Shelter Afforded", "F")), 1) * 7
    # Facilities
    for field in ["Supplies - Fuel Oil", "Supplies - Diesel Oil", "Supplies - Water",
                  "Repairs", "Dry Dock"]:
        val = str(row.get(field, "N"))
        if val in ("Y", "L", "M", "S"):
            score += 8
    return min(score, 100)


def derive_strategic_score(row: pd.Series) -> int:
    """Derive a 0-100 strategic score from WPI fields."""
    score = 0
    score += HARBOR_SIZE_MAP.get(str(row.get("Harbor Size", "S")), 1) * 12
    # Cargo capabilities
    for field in ["Cargo - Wharf - Container", "Cargo - Anchor - Container",
                  "Cargo - Wharf - Bulk", "Cargo - Wharf - Solid Bulk"]:
        val = str(row.get(field, "N"))
        if val in ("Y", "L", "M", "S"):
            score += 10
    # Max vessel size
    max_size = str(row.get("Max Vessel Size", ""))
    if max_size == "L":
        score += 20
    elif max_size == "M":
        score += 10
    return min(score, 100)


def get_cargo_capabilities(row: pd.Series) -> list:
    caps = []
    if str(row.get("Cargo - Wharf - Container", "N")) != "N":
        caps.append("Container")
    if str(row.get("Cargo - Wharf - Bulk", "N")) != "N":
        caps.append("Bulk")
    if str(row.get("Cargo - Wharf - Solid Bulk", "N")) != "N" and "Bulk" not in caps:
        caps.append("Bulk")
    # Default at least Container for major ports
    if not caps:
        caps.append("Container")
    return caps


def main():
    if not os.path.exists(RAW_PATH):
        print(f"WPI CSV not found at {RAW_PATH}")
        print("Using pre-built ports.json instead (download UpdatedPub150.csv for live processing)")
        return

    print(f"Reading WPI data from {RAW_PATH}...")
    df = pd.read_csv(RAW_PATH, encoding="latin-1", low_memory=False)

    # Normalize port name column
    name_col = None
    for col in df.columns:
        if "port name" in col.lower() or "main port name" in col.lower():
            name_col = col
            break

    if not name_col:
        print(f"Could not find port name column. Columns: {list(df.columns[:20])}")
        return

    df["_name_upper"] = df[name_col].str.upper().str.strip()

    ports = []
    for wpi_name, port_id in TARGET_PORTS.items():
        matches = df[df["_name_upper"] == wpi_name]
        if matches.empty:
            print(f"  WARNING: {wpi_name} not found in WPI data")
            continue

        row = matches.iloc[0]
        lat = float(row.get("Latitude", 0))
        lng = float(row.get("Longitude", 0))

        port = {
            "id": port_id,
            "name": str(row[name_col]).strip().title(),
            "country": str(row.get("Country", "Unknown")).strip(),
            "lat": lat,
            "lng": lng,
            "harbor_type": str(row.get("Harbor Type", "Unknown")),
            "cargo_capability": get_cargo_capabilities(row),
            "services_score": derive_services_score(row),
            "strategic_score": derive_strategic_score(row),
            "no2_mean": 0.0,  # Filled by process_no2.py
            "viirs_mean": 0.0,  # Filled by process_viirs.py
        }
        ports.append(port)
        print(f"  Processed: {port['name']} ({port_id}) — services={port['services_score']}, strategic={port['strategic_score']}")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(ports, f, indent=2)

    print(f"\nWrote {len(ports)} ports to {OUT_PATH}")


if __name__ == "__main__":
    main()
