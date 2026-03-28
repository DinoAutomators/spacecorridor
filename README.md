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

The app loads data from [processed_data](/Users/taimuradam/Documents/GitHub/spacecorridor/processed_data) by default. This matches the Person 1 → Person 2 handoff model: Person 1 owns raw data and feature preparation, while this backend starts from the frozen processed features.

You can point it at a different file or directory with:

```bash
export CORRIDORIQ_DATA_PATH=/absolute/path/to/processed_data
```

Supported inputs:

- `processed_data/corridor_features.csv`
- `processed_data/port_features.csv`
- or a bundled JSON file with `corridors` and `ports`

Minimum shared corridor fields, all normalized to `0-100`:

- `corridor_id`
- `corridor_name`
- `start_port`
- `end_port`
- `no2_score`
- `night_lights_score`
- `shipping_emissions_score`
- `port_readiness_score`
- `connectivity_score`
- `transition_feasibility_score`

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
- The scoring weights and rule thresholds are centralized in the domain modules so they are easy to tune once Person 1 freezes final feature values.
- Readiness is modeled as actionability, not just pollution magnitude: high pressure with weak delivery conditions is penalized, while high pressure plus strong leverage is rewarded.
