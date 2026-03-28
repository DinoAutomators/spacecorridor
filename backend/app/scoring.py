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
        weight=0.25,
        metric_keys=("shipping_emissions_score", "no2_score"),
        rationale="Shipping emissions context and NO2 pressure indicate whether the corridor faces meaningful decarbonization pressure.",
    ),
    ComponentDefinition(
        key="logistics_activity",
        label="Logistics Activity",
        weight=0.20,
        metric_keys=("night_lights_score",),
        rationale="Nighttime lights act as a persistent proxy for logistics activity and operational concentration.",
    ),
    ComponentDefinition(
        key="port_infrastructure_readiness",
        label="Port Infrastructure Readiness",
        weight=0.20,
        metric_keys=("port_readiness_score",),
        rationale="Port readiness captures whether endpoint infrastructure can support near-term decarbonization interventions.",
    ),
    ComponentDefinition(
        key="cross_mode_connectivity",
        label="Cross-Mode Connectivity",
        weight=0.20,
        metric_keys=("connectivity_score",),
        rationale="Connectivity reflects whether corridor decarbonization can extend beyond the port into the wider freight system.",
    ),
    ComponentDefinition(
        key="transition_feasibility",
        label="Transition Feasibility",
        weight=0.15,
        metric_keys=("transition_feasibility_score",),
        rationale="Transition feasibility estimates whether intervention is actionable in the near term, not just desirable.",
    ),
)


def _average(values: list[float]) -> float:
    return round(sum(values) / len(values), 2)


def component_scores(corridor: CorridorRecord) -> list[ScoreComponent]:
    features = corridor.model_dump()
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
    component_map = {component.key: component.score for component in components}
    emissions_score = component_map["emissions_pollution_intensity"]
    logistics_score = component_map["logistics_activity"]
    port_score = component_map["port_infrastructure_readiness"]
    connectivity_score = component_map["cross_mode_connectivity"]
    feasibility_score = component_map["transition_feasibility"]

    adjustments: list[str] = []
    leverage_average = round((port_score + connectivity_score + feasibility_score) / 3, 2)
    readiness_score = weighted

    if emissions_score >= 70 and leverage_average < 50:
        readiness_score -= 8
        adjustments.append(
            "High environmental pressure is being discounted because delivery conditions are still weak."
        )

    if emissions_score >= 65 and logistics_score >= 65 and leverage_average >= 60:
        readiness_score += 5
        adjustments.append(
            "Readiness is boosted because pressure, activity, and intervention leverage are all strong enough for near-term action."
        )

    readiness_score = round(max(0.0, min(100.0, readiness_score)), 2)
    strengths = [component.label for component in components if component.score >= 70]
    shortfalls = [component.label for component in components if component.score < 50]

    return CorridorScore(
        corridor_id=corridor.corridor_id,
        readiness_score=readiness_score,
        band=_band(readiness_score),
        components=components,
        strengths=strengths,
        shortfalls=shortfalls,
        adjustments=adjustments,
    )
