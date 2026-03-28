from __future__ import annotations

from .schemas import CorridorRecord, DiagnosisFinding, DiagnosisPanel
from .scoring import score_corridor


def diagnose_corridor(corridor: CorridorRecord) -> DiagnosisPanel:
    score = score_corridor(corridor)
    features = corridor.feature_table
    component_map = {component.key: component for component in score.components}
    findings: list[DiagnosisFinding] = []

    logistics_score = component_map["logistics_activity"].score
    port_score = component_map["port_infrastructure_readiness"].score
    emissions_score = component_map["emissions_pollution_intensity"].score
    connectivity_score = component_map["cross_mode_connectivity"].score
    feasibility_score = component_map["transition_feasibility"].score

    if logistics_score >= 70 and port_score < 50:
        findings.append(
            DiagnosisFinding(
                code="infrastructure_bottleneck",
                title="Infrastructure bottleneck",
                severity="high" if logistics_score - port_score >= 25 else "medium",
                summary="High activity is outrunning current port readiness, which points to infrastructure capacity and electrification gaps.",
                evidence={
                    "logistics_activity": logistics_score,
                    "port_infrastructure_readiness": port_score,
                },
                recommended_focus=["port electrification", "low-carbon fuel infrastructure"],
            )
        )

    if emissions_score >= 70 and connectivity_score < 50:
        findings.append(
            DiagnosisFinding(
                code="trucking_transition_bottleneck",
                title="Trucking transition bottleneck",
                severity="high",
                summary="The corridor has high emissions exposure but weak inland connectivity, making truck transition and intermodal shifts harder to execute.",
                evidence={
                    "emissions_pollution_intensity": emissions_score,
                    "cross_mode_connectivity": connectivity_score,
                },
                recommended_focus=["inland EV truck support", "cross-mode coordination investment"],
            )
        )

    if emissions_score >= 65 and features.low_carbon_fuel_index < 45:
        findings.append(
            DiagnosisFinding(
                code="fuel_network_gap",
                title="Fuel network gap",
                severity="medium",
                summary="Clean-fuel infrastructure readiness is lagging corridor need, which will constrain vessel, drayage, and terminal transition paths.",
                evidence={
                    "emissions_pollution_intensity": emissions_score,
                    "low_carbon_fuel_index": features.low_carbon_fuel_index,
                },
                recommended_focus=["low-carbon fuel infrastructure"],
            )
        )

    if features.cross_mode_coordination_index < 45 and logistics_score >= 60:
        findings.append(
            DiagnosisFinding(
                code="coordination_gap",
                title="Coordination gap",
                severity="medium",
                summary="Operational coordination across port, rail, and inland partners is too weak for the level of corridor activity.",
                evidence={
                    "logistics_activity": logistics_score,
                    "cross_mode_coordination_index": features.cross_mode_coordination_index,
                },
                recommended_focus=["cross-mode coordination investment"],
            )
        )

    if feasibility_score < 45 and score.overall_score >= 55:
        findings.append(
            DiagnosisFinding(
                code="execution_risk",
                title="Execution risk",
                severity="medium",
                summary="The corridor has enough strategic value to act now, but weak permitting, land, policy, or workforce readiness could delay execution.",
                evidence={"transition_feasibility": feasibility_score},
                recommended_focus=["delivery sequencing", "public-private coordination"],
            )
        )

    if not findings:
        findings.append(
            DiagnosisFinding(
                code="balanced_profile",
                title="Balanced profile",
                severity="low",
                summary="No major bottleneck dominates the corridor today; the best next step is targeted investment against the smallest readiness gaps.",
                evidence={"overall_score": score.overall_score},
                recommended_focus=["targeted optimization"],
            )
        )

    findings.sort(key=lambda finding: {"high": 0, "medium": 1, "low": 2}[finding.severity])
    summary = findings[0].summary
    return DiagnosisPanel(corridor_id=corridor.id, summary=summary, findings=findings)

