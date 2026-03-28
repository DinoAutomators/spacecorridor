"""
Google Earth Engine script: compute mean nighttime radiance per port buffer zone.

Input:  VIIRS Nighttime Lights (NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG)
Output: data/processed/viirs_stats.json

Requirements: pip install earthengine-api
              ee.Authenticate() + ee.Initialize() must be configured

For each of the 10 target ports, computes mean nighttime radiance
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

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "viirs_stats.json")

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

BUFFER_RADIUS_M = 25000


def compute_viirs_stats():
    if not HAS_EE:
        print("Skipping GEE processing (earthengine-api not available)")
        print("Using pre-computed viirs values in ports.json")
        return

    try:
        ee.Initialize()
    except Exception as e:
        print(f"Failed to initialize Earth Engine: {e}")
        print("Run ee.Authenticate() first, or use pre-computed data")
        return

    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    viirs_collection = (
        ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG")
        .filterDate(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        .select("avg_rad")
    )

    mean_radiance = viirs_collection.mean()

    results = {}
    for port in PORTS:
        point = ee.Geometry.Point([port["lng"], port["lat"]])
        buffer = point.buffer(BUFFER_RADIUS_M)

        stats = mean_radiance.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=buffer,
            scale=500,
            maxPixels=1e9,
        ).getInfo()

        radiance = stats.get("avg_rad", 0) or 0

        results[port["id"]] = {
            "viirs_mean": round(radiance, 2),
            "unit": "nW/cm²/sr",
            "buffer_radius_m": BUFFER_RADIUS_M,
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        }
        print(f"  {port['id']}: VIIRS mean radiance = {radiance:.2f} nW/cm²/sr")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nWrote VIIRS stats to {OUT_PATH}")


if __name__ == "__main__":
    compute_viirs_stats()
