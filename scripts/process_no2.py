"""
Google Earth Engine script: compute mean tropospheric NO2 per port buffer zone.

Input:  Sentinel-5P OFFL NO2 (COPERNICUS/S5P/OFFL/L3_NO2)
Output: data/processed/no2_stats.json

Requirements: pip install earthengine-api
              ee.Authenticate() + ee.Initialize() must be configured

For each of the 10 target ports, computes mean tropospheric NO2 column density
within a 25km buffer over the most recent 6-month period.
"""

import json
import os
from datetime import datetime, timedelta

try:
    import ee
    HAS_EE = True
except ImportError:
    HAS_EE = False
    print("earthengine-api not installed. Run: pip install earthengine-api")

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "no2_stats.json")

PORTS = [
    {"id": "singapore", "lat": 1.2644, "lng": 103.8222},
    {"id": "rotterdam", "lat": 51.9225, "lng": 4.47917},
    {"id": "shanghai", "lat": 31.2304, "lng": 121.4737},
    {"id": "los_angeles", "lat": 33.7405, "lng": -118.2653},
    {"id": "jebel_ali", "lat": 25.0177, "lng": 55.0607},
    {"id": "mumbai", "lat": 18.9489, "lng": 72.9518},
    {"id": "busan", "lat": 35.1028, "lng": 129.0403},
    {"id": "long_beach", "lat": 33.7544, "lng": -118.2166},
    {"id": "algeciras", "lat": 36.1275, "lng": -5.4428},
    {"id": "santos", "lat": -23.9608, "lng": -46.3336},
]

BUFFER_RADIUS_M = 25000  # 25km


def compute_no2_stats():
    if not HAS_EE:
        print("Skipping GEE processing (earthengine-api not available)")
        print("Using pre-computed no2 values in ports.json")
        return

    try:
        ee.Initialize()
    except Exception as e:
        print(f"Failed to initialize Earth Engine: {e}")
        print("Run ee.Authenticate() first, or use pre-computed data")
        return

    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    no2_collection = (
        ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
        .filterDate(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        .select("tropospheric_NO2_column_number_density")
    )

    mean_no2 = no2_collection.mean()

    results = {}
    for port in PORTS:
        point = ee.Geometry.Point([port["lng"], port["lat"]])
        buffer = point.buffer(BUFFER_RADIUS_M)

        stats = mean_no2.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=buffer,
            scale=1000,
            maxPixels=1e9,
        ).getInfo()

        no2_value = stats.get("tropospheric_NO2_column_number_density", 0)
        # Convert from mol/m² to µmol/m² for readability
        no2_umol = (no2_value or 0) * 1e6

        results[port["id"]] = {
            "no2_mean_mol_m2": no2_value,
            "no2_mean_umol_m2": round(no2_umol, 2),
            "buffer_radius_m": BUFFER_RADIUS_M,
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        }
        print(f"  {port['id']}: NO2 mean = {no2_umol:.2f} µmol/m²")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nWrote NO2 stats to {OUT_PATH}")


if __name__ == "__main__":
    compute_no2_stats()
