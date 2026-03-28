# Backend Setup

This backend is the product logic layer for CorridorIQ. It turns prepared corridor feature data into:

- readiness scores
- bottleneck diagnoses
- intervention recommendations
- frontend-ready corridor payloads

## Run locally

```bash
pip install -e .
uvicorn backend.app.main:app --reload
```

## Data handoff from Person 1

You can load either:

1. A single bundled JSON file containing both `corridors` and `ports`
2. A directory containing:
   - `corridors.json`
   - `ports.json`

Examples:

```bash
export CORRIDORIQ_DATA_PATH=/absolute/path/to/seed_data.json
uvicorn backend.app.main:app --reload
```

```bash
export CORRIDORIQ_DATA_PATH=/absolute/path/to/processed-data
uvicorn backend.app.main:app --reload
```

## Expected corridor feature fields

Each corridor must provide a `feature_table` object with:

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

All values should be normalized to `0-100`.

## API outputs for frontend

- `GET /corridors`: map-card payloads for ranking and map summaries
- `GET /corridors/{id}`: full detail payload for the corridor view
- `GET /ports`: endpoint list for map markers and filtering
- `GET /score/{corridor_id}`: score breakdown
- `GET /diagnosis/{corridor_id}`: diagnosis panel data
- `GET /recommendation/{corridor_id}`: recommendation panel data

## Frontend integration

Set `CORRIDORIQ_CORS_ORIGINS` if the frontend runs on another origin.

Example:

```bash
export CORRIDORIQ_CORS_ORIGINS=http://localhost:3000
```
