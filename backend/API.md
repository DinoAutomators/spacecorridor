# API Documentation

## Base behavior

All endpoints return JSON. Corridor responses are shaped for direct frontend use, especially for:

- map cards
- corridor detail views
- diagnosis panels
- recommendation panels

## Endpoints

### `GET /health`

Returns a simple service health payload.

### `GET /corridors`

Returns a list of `map_cards` plus corridor count.

Example response shape:

```json
{
  "count": 3,
  "items": [
    {
      "corridor_id": "pacific-gateway",
      "corridor_name": "Pacific Gateway",
      "origin": "Los Angeles, CA",
      "destination": "Phoenix, AZ",
      "score": 63.25,
      "band": "ready",
      "top_diagnosis": "Infrastructure bottleneck",
      "top_recommendation": "Port electrification",
      "center": {
        "lat": 33.85,
        "lon": -116.2
      }
    }
  ]
}
```

### `GET /corridors/{id}`

Returns the corridor detail view:

- corridor metadata
- related ports
- score block
- diagnosis panel
- recommendation panel
- map card summary

### `GET /ports`

Returns all ports. Supports optional query parameter `corridor_id`.

### `GET /score/{corridor_id}`

Returns:

- overall score
- score band
- weighted component breakdown
- strengths
- shortfalls

### `GET /diagnosis/{corridor_id}`

Returns:

- summary sentence
- ordered diagnostic findings
- evidence for each rule that fired

### `GET /recommendation/{corridor_id}`

Returns:

- summary sentence
- ordered recommendations
- priorities
- triggered findings
- target metrics

## Tuning model behavior

Scoring weights live in:

- [backend/app/scoring.py](/Users/taimuradam/Documents/GitHub/spacecorridor/backend/app/scoring.py)

Diagnosis rules live in:

- [backend/app/diagnosis.py](/Users/taimuradam/Documents/GitHub/spacecorridor/backend/app/diagnosis.py)

Recommendation rules live in:

- [backend/app/recommendation.py](/Users/taimuradam/Documents/GitHub/spacecorridor/backend/app/recommendation.py)

