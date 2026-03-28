"""
Parse OECD Maritime Transport CO2 Emissions CSV → emissions scores per corridor.

Input:  data/raw/oecd_maritime_co2.csv
Output: Updates corridor data with emissions context

The OECD data provides CO2 emissions by country and ship type.
We map corridor endpoint countries to their emissions intensity
and normalize to a 0-100 score (higher = cleaner = more ready).
"""

import json
import os
import pandas as pd

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "oecd_maritime_co2.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "oecd_emissions.json")

# Country mapping for corridors
CORRIDOR_COUNTRIES = {
    "singapore-rotterdam": ["Singapore", "Netherlands"],
    "shanghai-los_angeles": ["China", "United States"],
    "jebel_ali-mumbai": ["United Arab Emirates", "India"],
    "busan-long_beach": ["Korea", "United States"],
    "algeciras-santos": ["Spain", "Brazil"],
}


def main():
    if not os.path.exists(RAW_PATH):
        print(f"OECD CSV not found at {RAW_PATH}")
        print("Using pre-computed emissions scores in corridor_scores.json")
        print("Download OECD maritime CO2 data for live processing")
        return

    print(f"Reading OECD data from {RAW_PATH}...")
    df = pd.read_csv(RAW_PATH, low_memory=False)

    print(f"Columns: {list(df.columns)}")
    print(f"Shape: {df.shape}")

    # Look for relevant columns (OECD CSVs vary in format)
    # Typically: COUNTRY, TIME, Value, VARIABLE
    country_col = None
    value_col = None
    for col in df.columns:
        if "country" in col.lower() or "cou" in col.lower():
            country_col = col
        if "value" in col.lower() or "obs" in col.lower():
            value_col = col

    if not country_col or not value_col:
        print("Could not identify country/value columns")
        return

    # Get latest year emissions per country
    results = {}
    for corridor_id, countries in CORRIDOR_COUNTRIES.items():
        total_emissions = 0
        for country in countries:
            matches = df[df[country_col].str.contains(country, case=False, na=False)]
            if not matches.empty:
                country_emissions = matches[value_col].mean()
                total_emissions += country_emissions
                print(f"  {corridor_id}: {country} avg emissions = {country_emissions:.2f}")

        results[corridor_id] = {
            "raw_emissions": total_emissions,
            "country_pair": countries,
        }

    # Normalize to 0-100 (invert: lower emissions = higher score)
    if results:
        max_emissions = max(r["raw_emissions"] for r in results.values()) or 1
        for corridor_id, data in results.items():
            data["emissions_score"] = round(100 * (1 - data["raw_emissions"] / max_emissions))

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nWrote emissions data to {OUT_PATH}")


if __name__ == "__main__":
    main()
