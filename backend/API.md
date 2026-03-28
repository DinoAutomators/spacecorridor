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
      "start_port": "port_los_angeles",
      "end_port": "port_phoenix_inland",
      "readiness_score": 64.4,
      "no2_score": 74,
      "night_lights_score": 88,
      "band": "emerging",
      "bottleneck_label": "Port Infrastructure Gap",
      "top_recommendation": "Port electrification",
      "center": {
        "lat": 33.59,
        "lon": -115.17
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
- `ai_explanation` for immediate frontend compatibility
- `ai_explanations` with selectable `concise`, `analyst`, and `executive` variants
- map card summary

Supports optional query parameter `explanation_variant` to choose which explanation variant is returned as `ai_explanation`.

### `GET /ports`

Returns all ports. Supports optional query parameter `corridor_id`.

### `GET /score/{corridor_id}`

Returns:

- readiness score
- score band
- weighted component breakdown
- strengths
- shortfalls
- actionability adjustments

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

## AI explanation layer

The detail endpoint adds a server-side explanation layer that:

- keeps scores, diagnoses, and recommendations rule-based
- generates structured explanation variants from OpenAI when enabled
- falls back to deterministic template text if AI is disabled, unavailable, or fails validation

Environment variables:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `CORRIDORIQ_AI_ENABLED`
- `CORRIDORIQ_AI_TIMEOUT_SECONDS`
- `CORRIDORIQ_AI_VARIANT_COUNT`
- `CORRIDORIQ_AI_PROMPT_VERSION`

## Tuning model behavior

Scoring weights live in:

- [backend/app/scoring.py](/Users/taimuradam/Documents/GitHub/spacecorridor/backend/app/scoring.py)

Diagnosis rules live in:

- [backend/app/diagnosis.py](/Users/taimuradam/Documents/GitHub/spacecorridor/backend/app/diagnosis.py)

Recommendation rules live in:

- [backend/app/recommendation.py](/Users/taimuradam/Documents/GitHub/spacecorridor/backend/app/recommendation.py)

## Shared contract

The backend is built around the Person 1 freeze-point contract documented in [processed_data/data_dictionary.md](/Users/taimuradam/Documents/GitHub/spacecorridor/processed_data/data_dictionary.md).
