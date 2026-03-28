"""Define the 5 MVP corridors with metadata.

IDs and structure match the frontend convention (data/processed/corridors.json).
"""
from __future__ import annotations

CORRIDOR_DEFINITIONS: list[dict] = [
    {
        "corridor_id": "singapore-rotterdam",
        "corridor_name": "Singapore \u2192 Rotterdam",
        "start_port_id": "singapore",
        "end_port_id": "rotterdam",
        "start_country_code": "SGP",
        "end_country_code": "NLD",
        "region": "Asia-Europe",
        "mode": "maritime",
        "time_period": "2024",
        "description": "The busiest global trade lane, connecting Southeast Asia's largest transshipment hub to Europe's primary gateway port through the Strait of Malacca and Suez Canal.",
        "strategic_importance_note": "Handles a major share of Asia-Europe container traffic through the Strait of Malacca and Suez Canal.",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [103.822, 1.264], [98.5, 3.5], [80.2, 6.8], [72.8, 10.5],
                [55.3, 12.8], [43.2, 12.5], [39.5, 15.5], [32.5, 30.0],
                [32.3, 31.3], [28.0, 35.0], [15.0, 37.5], [5.0, 39.0],
                [-3.0, 43.0], [-5.0, 48.0], [0.0, 50.5], [4.479, 51.922],
            ],
        },
    },
    {
        "corridor_id": "shanghai-los_angeles",
        "corridor_name": "Shanghai \u2192 Los Angeles",
        "start_port_id": "shanghai",
        "end_port_id": "los_angeles",
        "start_country_code": "CHN",
        "end_country_code": "USA",
        "region": "Trans-Pacific",
        "mode": "maritime",
        "time_period": "2024",
        "description": "Major trans-Pacific route carrying electronics, machinery, and consumer goods from China's largest port to the U.S. West Coast.",
        "strategic_importance_note": "Carries the highest container volume of any trans-Pacific route, critical for US consumer goods supply.",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [121.474, 31.230], [130.0, 33.0], [140.0, 35.0], [155.0, 38.0],
                [170.0, 40.0], [-180.0, 42.0], [-165.0, 40.0], [-150.0, 38.0],
                [-135.0, 35.5], [-125.0, 34.0], [-118.265, 33.740],
            ],
        },
    },
    {
        "corridor_id": "jebel_ali-mumbai",
        "corridor_name": "Jebel Ali \u2192 Mumbai",
        "start_port_id": "jebel_ali",
        "end_port_id": "mumbai",
        "start_country_code": "ARE",
        "end_country_code": "IND",
        "region": "Regional",
        "mode": "maritime",
        "time_period": "2024",
        "description": "High-intensity regional corridor connecting the UAE's premier port to India's busiest container terminal, carrying petroleum products and manufactured goods.",
        "strategic_importance_note": "Handles significant container, petroleum, and general cargo traffic across the Arabian Sea.",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [55.061, 25.018], [56.5, 24.5], [58.5, 23.0],
                [62.0, 22.0], [66.0, 21.5], [69.0, 20.0], [72.952, 18.949],
            ],
        },
    },
    {
        "corridor_id": "busan-long_beach",
        "corridor_name": "Busan \u2192 Long Beach",
        "start_port_id": "busan",
        "end_port_id": "long_beach",
        "start_country_code": "KOR",
        "end_country_code": "USA",
        "region": "Trans-Pacific",
        "mode": "maritime",
        "time_period": "2024",
        "description": "Key Asia-Americas route connecting South Korea's largest port to the Port of Long Beach, a major U.S. import gateway.",
        "strategic_importance_note": "Critical route for South Korean electronics, automotive, and machinery exports to the Americas.",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [129.040, 35.103], [140.0, 37.0], [155.0, 40.0], [170.0, 42.0],
                [-180.0, 43.0], [-165.0, 41.0], [-150.0, 39.0],
                [-135.0, 36.0], [-125.0, 34.5], [-118.217, 33.754],
            ],
        },
    },
    {
        "corridor_id": "algeciras-santos",
        "corridor_name": "Algeciras \u2192 Santos",
        "start_port_id": "algeciras",
        "end_port_id": "santos",
        "start_country_code": "ESP",
        "end_country_code": "BRA",
        "region": "Atlantic",
        "mode": "maritime",
        "time_period": "2024",
        "description": "Europe-South America trade link connecting Spain's busiest port to Brazil's largest, carrying automotive parts, agricultural products, and manufactured goods.",
        "strategic_importance_note": "Key route for Brazilian commodity exports (soy, sugar, coffee, iron ore) to the European market.",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [-5.443, 36.128], [-10.0, 32.0], [-15.0, 28.0], [-18.0, 22.0],
                [-22.0, 15.0], [-28.0, 5.0], [-32.0, -5.0],
                [-36.0, -12.0], [-40.0, -18.0], [-46.334, -23.961],
            ],
        },
    },
]
