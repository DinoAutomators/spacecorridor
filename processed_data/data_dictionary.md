# Processed Data Contract

This folder represents the freeze-point handoff from Person 1 to Person 2.

## `corridor_features.csv`

Required columns:

- `corridor_id`
- `corridor_name`
- `start_port`
- `end_port`
- `region`
- `no2_score`
- `night_lights_score`
- `shipping_emissions_score`
- `port_readiness_score`
- `connectivity_score`
- `transition_feasibility_score`

Recommended supporting columns:

- `mode`
- `time_period`
- `description`
- `strategic_importance_note`
- `geometry`

All score columns should be normalized to `0-100`.

## `port_features.csv`

Recommended columns:

- `port_id`
- `port_name`
- `country`
- `region`
- `mode`
- `lat`
- `lon`
- `harbor_type`
- `cargo_capability`
- `services_score`
- `strategic_score`
- `readiness_score`
