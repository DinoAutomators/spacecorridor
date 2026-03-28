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

1. A directory containing:
   - `corridor_features.csv`
   - `port_features.csv`
2. A single bundled JSON file containing both `corridors` and `ports`

Examples:

```bash
export CORRIDORIQ_DATA_PATH=/absolute/path/to/processed_data
uvicorn backend.app.main:app --reload
```

```bash
export CORRIDORIQ_DATA_PATH=/absolute/path/to/feature-bundle.json
uvicorn backend.app.main:app --reload
```

## Expected corridor feature fields

Each corridor must provide the shared fixed columns below:

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

All values should be normalized to `0-100`.

Recommended supporting columns:

- `region`
- `mode`
- `time_period`
- `description`
- `strategic_importance_note`
- `geometry`

This keeps the overlap clean:

- Person 1 owns raw collection, cleaning, and feature generation
- Person 2 owns score calculation, diagnosis, recommendations, and API delivery

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

## Decision logic included

The backend currently implements:

- readiness scoring across emissions/pollution intensity, logistics activity, port infrastructure readiness, cross-mode connectivity, and transition feasibility
- diagnosis rules for port infrastructure gaps, trucking transition bottlenecks, fuel transition gaps, pollution exposure hotspots, cross-mode coordination gaps, and monitoring/readiness gaps
- recommendation rules for port electrification, low-carbon fuel infrastructure, inland EV truck support, cross-mode coordination investment, hotspot mitigation, and phased monitoring
