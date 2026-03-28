"""Load cleaned data into Supabase tables.

Matches the schema from supabase/migrations/001_schema.sql:
  - ports: id, name, country, lat, lng, harbor_type, cargo_capability[], services_score, strategic_score, no2_mean, viirs_mean
  - corridors: id, name, from_port_id, to_port_id, region, geometry, description
  - corridor_scores: id, corridor_id, emissions_score, no2_score, lights_score, strategic_score, feasibility_score, readiness_score, bottleneck, recommendation, ai_explanation
"""
from __future__ import annotations

import json

from pipeline.config import SUPABASE_SERVICE_KEY, SUPABASE_URL


def _get_client():
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env to load data into Supabase."
        )
    from supabase import create_client

    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def load_ports(ports: list[dict]) -> int:
    """Upsert port records into the ports table."""
    client = _get_client()
    rows = []
    for p in ports:
        rows.append({
            "id": p["port_id"],
            "name": p["port_name"],
            "country": p["country"],
            "lat": float(p["lat"]),
            "lng": float(p["lon"]),
            "harbor_type": p.get("harbor_type", ""),
            "cargo_capability": ["Container", "Bulk", "Tanker"],
            "services_score": int(round(float(p.get("services_score", 50)))),
            "strategic_score": int(round(float(p.get("strategic_score", 50)))),
            "no2_mean": 0.0,
            "viirs_mean": 0.0,
        })
    result = client.table("ports").upsert(rows, on_conflict="id").execute()
    return len(result.data)


def load_corridors(corridors: list[dict]) -> int:
    """Upsert corridor records into the corridors table."""
    client = _get_client()
    rows = []
    for c in corridors:
        geometry = c.get("geometry", {})
        if isinstance(geometry, str):
            geometry = json.loads(geometry)
        if isinstance(geometry, list):
            geometry = {"type": "LineString", "coordinates": geometry}
        rows.append({
            "id": c.get("corridor_id", ""),
            "name": c.get("corridor_name", ""),
            "from_port_id": c.get("start_port", c.get("start_port_id", "")),
            "to_port_id": c.get("end_port", c.get("end_port_id", "")),
            "region": c.get("region", ""),
            "geometry": geometry,
            "description": c.get("description", ""),
        })
    result = client.table("corridors").upsert(rows, on_conflict="id").execute()
    return len(result.data)


def load_corridor_scores(scores: list[dict]) -> int:
    """Upsert corridor score records into the corridor_scores table."""
    client = _get_client()
    result = client.table("corridor_scores").upsert(scores, on_conflict="id").execute()
    return len(result.data)
