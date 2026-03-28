from __future__ import annotations

from dataclasses import dataclass

from .schemas import CorridorRecord, CorridorScore, ScoreComponent


@dataclass(frozen=True)
class ComponentDefinition:
    key: str
    label: str
    weight: float
    metric_keys: tuple[str, ...]
    rationale: str


COMPONENTS: tuple[ComponentDefinition, ...] = (
    ComponentDefinition(
        key="emissions_pollution_intensity",
        label="Emissions / Pollution Intensity",
        weight=0.20,
        metric_keys=("emissions_intensity_index", "pollution_burden_index"),
        rationale="Higher emissions and pollution burdens increase the value of intervention in the corridor.",
    ),
    ComponentDefinition(
        key="logistics_activity",
        label="Logistics Activity",
        weight=0.20,
        metric_keys=("freight_volume_index", "throughput_index"),
        rationale="Higher freight demand and throughput make interventions more material to network performance.",
    ),
    ComponentDefinition(
        key="port_infrastructure_readiness",
        label="Port Infrastructure Readiness",
        weight=0.25,
        metric_keys=("port_capacity_index", "port_electrification_index", "low_carbon_fuel_index"),
        rationale="Port capacity and clean-energy infrastructure determine whether the corridor can absorb transition investments.",
    ),
    ComponentDefinition(
        key="cross_mode_connectivity",
        label="Cross-Mode Connectivity",
        weight=0.20,
        metric_keys=("rail_connectivity_index", "inland_ev_support_index", "cross_mode_coordination_index"),
        rationale="Intermodal coordination and inland support determine whether activity can shift cleanly across the network.",
    ),
    ComponentDefinition(
        key="transition_feasibility",
        label="Transition Feasibility",
        weight=0.15,
        metric_keys=(
            "policy_support_index",
            "permitting_readiness_index",
            "land_availability_index",
            "workforce_readiness_index",
        ),
        rationale="Policy, permitting, land, and workforce readiness shape execution speed and delivery risk.",
    ),
)


def _average(values: list[float]) -> float:
    return round(sum(values) / len(values), 2)


def component_scores(corridor: CorridorRecord) -> list[ScoreComponent]:
    features = corridor.feature_table.model_dump()
    components: list[ScoreComponent] = []
    for definition in COMPONENTS:
        metrics = {metric: float(features[metric]) for metric in definition.metric_keys}
        score = _average(list(metrics.values()))
        components.append(
            ScoreComponent(
                key=definition.key,
                label=definition.label,
                score=score,
                weight=definition.weight,
                metrics=metrics,
                rationale=definition.rationale,
            )
        )
    return components


def _band(overall_score: float) -> str:
    if overall_score >= 80:
        return "leading"
    if overall_score >= 65:
        return "ready"
    if overall_score >= 50:
        return "emerging"
    return "constrained"


def score_corridor(corridor: CorridorRecord) -> CorridorScore:
    components = component_scores(corridor)
    weighted = sum(component.score * component.weight for component in components)
    overall_score = round(weighted, 2)
    strengths = [component.label for component in components if component.score >= 70]
    shortfalls = [component.label for component in components if component.score < 50]

    return CorridorScore(
        corridor_id=corridor.id,
        overall_score=overall_score,
        band=_band(overall_score),
        components=components,
        strengths=strengths,
        shortfalls=shortfalls,
    )

