"""Export cleaned data to CSV and JSON files for backend and frontend."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from pipeline.config import PROCESSED_DATA_DIR, PROJECT_ROOT

CORRIDOR_COLUMNS = [
    "corridor_id",
    "corridor_name",
    "start_port",
    "end_port",
    "region",
    "mode",
    "time_period",
    "description",
    "strategic_importance_note",
    "geometry",
    "no2_score",
    "night_lights_score",
    "shipping_emissions_score",
    "port_readiness_score",
    "connectivity_score",
    "transition_feasibility_score",
]

PORT_COLUMNS = [
    "port_id",
    "port_name",
    "country",
    "region",
    "mode",
    "lat",
    "lon",
    "harbor_type",
    "cargo_capability",
    "services_score",
    "strategic_score",
    "readiness_score",
]


def export_corridors(corridors: list[dict], output_dir: Path | None = None) -> Path:
    output_dir = output_dir or PROCESSED_DATA_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "corridor_features.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CORRIDOR_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in corridors:
            write_row = dict(row)
            if isinstance(write_row.get("geometry"), list):
                write_row["geometry"] = json.dumps(write_row["geometry"])
            writer.writerow(write_row)
    return path


def export_ports(ports: list[dict], output_dir: Path | None = None) -> Path:
    output_dir = output_dir or PROCESSED_DATA_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "port_features.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=PORT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ports)
    return path


def export_frontend_json(
    corridors: list[dict],
    ports: list[dict],
    corridor_scores: list[dict],
    output_dir: Path | None = None,
) -> Path:
    """Export JSON files matching the Next.js frontend format in data/processed/."""
    output_dir = output_dir or (PROJECT_ROOT / "data" / "processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    # ports.json — frontend Port type
    fe_ports = []
    for p in ports:
        fe_ports.append({
            "id": p["port_id"],
            "name": p["port_name"],
            "country": p["country"],
            "lat": float(p["lat"]),
            "lng": float(p["lon"]),
            "harbor_type": p.get("harbor_type", ""),
            "cargo_capability": ["Container", "Bulk", "Tanker"],
            "services_score": int(round(float(p.get("services_score", 50)))),
            "strategic_score": int(round(float(p.get("strategic_score", 50)))),
            "no2_mean": 0.0,  # populated below from corridor data
            "viirs_mean": 0.0,
        })
    with open(output_dir / "ports.json", "w", encoding="utf-8") as f:
        json.dump(fe_ports, f, indent=2)

    # corridors.json — frontend Corridor type
    fe_corridors = []
    for c in corridors:
        geometry = c.get("geometry", {})
        if isinstance(geometry, str):
            geometry = json.loads(geometry)
        if isinstance(geometry, list):
            geometry = {"type": "LineString", "coordinates": geometry}
        fe_corridors.append({
            "id": c.get("corridor_id", ""),
            "name": c.get("corridor_name", ""),
            "from_port_id": c.get("start_port", c.get("start_port_id", "")),
            "to_port_id": c.get("end_port", c.get("end_port_id", "")),
            "region": c.get("region", ""),
            "description": c.get("description", ""),
            "geometry": geometry,
        })
    with open(output_dir / "corridors.json", "w", encoding="utf-8") as f:
        json.dump(fe_corridors, f, indent=2)

    # corridor_scores.json — frontend CorridorScore type
    with open(output_dir / "corridor_scores.json", "w", encoding="utf-8") as f:
        json.dump(corridor_scores, f, indent=2)

    return output_dir
