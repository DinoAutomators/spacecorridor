from __future__ import annotations

from .diagnosis import diagnose_corridor
from .schemas import CorridorRecord, RecommendationItem, RecommendationPanel


def recommend_for_corridor(corridor: CorridorRecord) -> RecommendationPanel:
    diagnosis = diagnose_corridor(corridor)
    features = corridor.feature_table
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
        "infrastructure_bottleneck" in finding_codes
        or features.port_electrification_index < 55
        or features.port_capacity_index < 50
    ):
        add_recommendation(
            RecommendationItem(
                code="port_electrification",
                title="Port electrification",
                priority="high" if features.port_electrification_index < 45 else "medium",
                summary="Upgrade terminal power, charging, and berth-side electrical systems to match corridor demand.",
                rationale="Electrification closes the port-side infrastructure gap that currently limits throughput and decarbonization readiness.",
                triggered_by=["infrastructure_bottleneck"],
                target_metrics=["port_electrification_index", "port_capacity_index"],
            )
        )

    if "fuel_network_gap" in finding_codes or features.low_carbon_fuel_index < 55:
        add_recommendation(
            RecommendationItem(
                code="low_carbon_fuel_infrastructure",
                title="Low-carbon fuel infrastructure",
                priority="high" if features.low_carbon_fuel_index < 40 else "medium",
                summary="Develop clean-fuel storage, bunkering, and terminal handling capacity for corridor operations.",
                rationale="Fuel network readiness is a hard dependency for maritime and drayage transition pathways.",
                triggered_by=["fuel_network_gap", "infrastructure_bottleneck"],
                target_metrics=["low_carbon_fuel_index"],
            )
        )

    if (
        "trucking_transition_bottleneck" in finding_codes
        or features.inland_ev_support_index < 55
        or features.rail_connectivity_index < 50
    ):
        add_recommendation(
            RecommendationItem(
                code="inland_ev_truck_support",
                title="Inland EV truck support",
                priority="high" if features.inland_ev_support_index < 45 else "medium",
                summary="Expand charging, staging, and fleet support at inland nodes to enable cleaner truck movement beyond the port.",
                rationale="Truck transition cannot scale if inland charging and operational support remain weak.",
                triggered_by=["trucking_transition_bottleneck"],
                target_metrics=["inland_ev_support_index", "rail_connectivity_index"],
            )
        )

    if "coordination_gap" in finding_codes or features.cross_mode_coordination_index < 55:
        add_recommendation(
            RecommendationItem(
                code="cross_mode_coordination_investment",
                title="Cross-mode coordination investment",
                priority="high" if features.cross_mode_coordination_index < 40 else "medium",
                summary="Fund shared planning, dispatch, and handoff processes across port, rail, and inland operators.",
                rationale="Better coordination increases asset utilization and makes corridor transition investments stick operationally.",
                triggered_by=["coordination_gap", "trucking_transition_bottleneck"],
                target_metrics=["cross_mode_coordination_index", "rail_connectivity_index"],
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
                triggered_by=["balanced_profile"],
                target_metrics=["overall_score"],
            )
        )

    ordered = sorted(
        recommendations.values(),
        key=lambda item: {"high": 0, "medium": 1, "low": 2}[item.priority],
    )
    summary = ordered[0].summary
    return RecommendationPanel(corridor_id=corridor.id, summary=summary, recommendations=ordered)

