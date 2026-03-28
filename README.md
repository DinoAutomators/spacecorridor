# CorridorIQ Backend

This repository now contains a FastAPI backend that turns prepared corridor feature data into product-ready outputs for CorridorIQ.

## What it includes

- Backend service with FastAPI
- Corridor scoring engine
- Bottleneck diagnosis logic
- Intervention recommendation logic
- Frontend-ready JSON for map cards, detail views, diagnosis panels, and recommendation panels
- OpenAPI docs at `/docs`

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn backend.app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/docs` for Swagger UI
- `http://127.0.0.1:8000/redoc` for ReDoc

## Data contract

The app loads data from `backend/data/seed_data.json` by default. You can point it at a different file with:

```bash
export CORRIDORIQ_DATA_PATH=/absolute/path/to/your-feature-data.json
```

The JSON file should contain:

- `corridors`: a list of corridor objects
- `ports`: a list of port objects

Each corridor expects the feature indices below, all on a `0-100` scale:

- `emissions_intensity_index`
- `pollution_burden_index`
- `freight_volume_index`
- `throughput_index`
- `port_capacity_index`
- `port_electrification_index`
- `low_carbon_fuel_index`
- `rail_connectivity_index`
- `inland_ev_support_index`
- `cross_mode_coordination_index`
- `policy_support_index`
- `permitting_readiness_index`
- `land_availability_index`
- `workforce_readiness_index`

## API routes

- `GET /health`
- `GET /corridors`
- `GET /corridors/{id}`
- `GET /ports`
- `GET /score/{corridor_id}`
- `GET /diagnosis/{corridor_id}`
- `GET /recommendation/{corridor_id}`

More route details and example payloads are in [backend/API.md](/Users/taimuradam/Documents/GitHub/spacecorridor/backend/API.md).

## Notes

- FastAPI automatically generates API documentation from the response models.
- The scoring weights and rule thresholds are centralized in the domain modules so they are easy to tune once Person 1's final feature tables arrive.

