from __future__ import annotations

from .diagnosis import diagnose_corridor
from .schemas import CorridorRecord, RecommendationItem, RecommendationPanel


def recommend_for_corridor(corridor: CorridorRecord) -> RecommendationPanel:
    diagnosis = diagnose_corridor(corridor)
    recommendations: dict[str, RecommendationItem] = {}

    def add_recommendation(item: RecommendationItem) -> None:
        existing = recommendations.get(item.code)
        if existing is None:
            recommendations[item.code] = item
            return
        if existing.priority == "medium" and item.priority == "high":
            recommendations[item.code] = item

    finding_codes = {finding.code for finding in diagnosis.findings}

    if (
        "port_infrastructure_gap" in finding_codes
        or corridor.port_readiness_score < 55
    ):
        add_recommendation(
            RecommendationItem(
                code="port_electrification",
                title="Port electrification",
                priority="high" if corridor.port_readiness_score < 45 else "medium",
                summary="Upgrade terminal power, charging, and berth-side electrical systems to match corridor demand.",
                rationale="Electrification closes the port-side infrastructure gap that currently limits throughput and decarbonization readiness.",
                triggered_by=["port_infrastructure_gap"],
                target_metrics=["port_readiness_score"],
            )
        )

    if "fuel_transition_gap" in finding_codes or corridor.shipping_emissions_score >= 70:
        add_recommendation(
            RecommendationItem(
                code="low_carbon_fuel_infrastructure",
                title="Low-carbon fuel infrastructure",
                priority="high" if "fuel_transition_gap" in finding_codes else "medium",
                summary="Develop clean-fuel storage, bunkering, and terminal handling capacity for corridor operations.",
                rationale="Fuel network readiness is a hard dependency for maritime and drayage transition pathways.",
                triggered_by=["fuel_transition_gap", "port_infrastructure_gap"],
                target_metrics=["shipping_emissions_score", "port_readiness_score"],
            )
        )

    if (
        "trucking_transition_bottleneck" in finding_codes
        or corridor.connectivity_score < 50
    ):
        add_recommendation(
            RecommendationItem(
                code="inland_ev_truck_support",
                title="Inland EV truck support",
                priority="high" if corridor.connectivity_score < 40 else "medium",
                summary="Expand charging, staging, and fleet support at inland nodes to enable cleaner truck movement beyond the port.",
                rationale="Truck transition cannot scale if inland charging and operational support remain weak.",
                triggered_by=["trucking_transition_bottleneck"],
                target_metrics=["connectivity_score"],
            )
        )

    if "cross_mode_coordination_gap" in finding_codes or corridor.connectivity_score < 55:
        add_recommendation(
            RecommendationItem(
                code="cross_mode_coordination_investment",
                title="Cross-mode coordination investment",
                priority="high" if corridor.connectivity_score < 40 else "medium",
                summary="Fund shared planning, dispatch, and handoff processes across port, rail, and inland operators.",
                rationale="Better coordination increases asset utilization and makes corridor transition investments stick operationally.",
                triggered_by=["cross_mode_coordination_gap", "trucking_transition_bottleneck"],
                target_metrics=["connectivity_score"],
            )
        )

    if "pollution_exposure_hotspot" in finding_codes:
        add_recommendation(
            RecommendationItem(
                code="endpoint_hotspot_mitigation",
                title="Endpoint hotspot mitigation",
                priority="high",
                summary="Prioritize near-term emissions reduction and air-quality mitigation at the corridor's highest-pressure ports.",
                rationale="Visible NO2 concentration around active endpoints suggests targeted local mitigation can produce the fastest public-health benefit.",
                triggered_by=["pollution_exposure_hotspot"],
                target_metrics=["no2_score", "port_readiness_score"],
            )
        )

    if "monitoring_readiness_gap" in finding_codes:
        add_recommendation(
            RecommendationItem(
                code="phased_monitoring_plan",
                title="Phased monitoring plan",
                priority="medium",
                summary="Improve corridor-specific monitoring and stage interventions in phases before committing to larger capital programs.",
                rationale="The corridor needs better signal clarity and readiness validation before the first intervention can be prioritized confidently.",
                triggered_by=["monitoring_readiness_gap"],
                target_metrics=["transition_feasibility_score", "connectivity_score"],
            )
        )

    if not recommendations:
        add_recommendation(
            RecommendationItem(
                code="targeted_gap_closure",
                title="Targeted gap closure",
                priority="low",
                summary="Focus the next round of investment on the lowest-scoring component rather than launching a broad corridor program.",
                rationale="The corridor is relatively balanced, so the highest return comes from precise gap closure instead of blanket spend.",
                triggered_by=["balanced_opportunity_profile"],
                target_metrics=["readiness_score"],
            )
        )

    ordered = sorted(
        recommendations.values(),
        key=lambda item: {"high": 0, "medium": 1, "low": 2}[item.priority],
    )
    summary = ordered[0].summary
    return RecommendationPanel(corridor_id=corridor.corridor_id, summary=summary, recommendations=ordered)
