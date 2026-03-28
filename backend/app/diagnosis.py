from __future__ import annotations

from .schemas import CorridorRecord, DiagnosisFinding, DiagnosisPanel
from .scoring import score_corridor


def diagnose_corridor(corridor: CorridorRecord) -> DiagnosisPanel:
    score = score_corridor(corridor)
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
                code="port_infrastructure_gap",
                title="Port Infrastructure Gap",
                severity="high" if logistics_score - port_score >= 25 else "medium",
                summary="High logistics activity is outrunning port readiness, which suggests endpoint electrification and terminal modernization are lagging corridor demand.",
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
                title="Trucking Transition Bottleneck",
                severity="high",
                summary="Environmental pressure is high, but weak inland connectivity is limiting cleaner truck flows and cross-network transition.",
                evidence={
                    "emissions_pollution_intensity": emissions_score,
                    "cross_mode_connectivity": connectivity_score,
                },
                recommended_focus=["inland EV truck support", "cross-mode coordination investment"],
            )
        )

    if corridor.shipping_emissions_score >= 70 and port_score >= 55 and feasibility_score >= 55:
        findings.append(
            DiagnosisFinding(
                code="fuel_transition_gap",
                title="Fuel Transition Gap",
                severity="medium",
                summary="The corridor is strategically active enough to act, but it likely needs cleaner-fuel readiness rather than basic corridor identification.",
                evidence={
                    "shipping_emissions_score": corridor.shipping_emissions_score,
                    "port_infrastructure_readiness": port_score,
                    "transition_feasibility": feasibility_score,
                },
                recommended_focus=["low-carbon fuel infrastructure"],
            )
        )

    if logistics_score >= 65 and connectivity_score < 55:
        findings.append(
            DiagnosisFinding(
                code="cross_mode_coordination_gap",
                title="Cross-Mode Coordination Gap",
                severity="medium",
                summary="The corridor is active, but port-to-inland coordination looks too weak for decarbonization measures to scale smoothly.",
                evidence={
                    "logistics_activity": logistics_score,
                    "cross_mode_connectivity": connectivity_score,
                },
                recommended_focus=["cross-mode coordination investment"],
            )
        )

    if corridor.no2_score >= 75 and corridor.night_lights_score >= 70 and port_score < 60:
        findings.append(
            DiagnosisFinding(
                code="pollution_exposure_hotspot",
                title="Pollution Exposure Hotspot",
                severity="medium",
                summary="Concentrated NO2 pressure around an active corridor suggests an endpoint hotspot where visible emissions mitigation may be needed quickly.",
                evidence={
                    "no2_score": corridor.no2_score,
                    "night_lights_score": corridor.night_lights_score,
                    "port_infrastructure_readiness": port_score,
                },
                recommended_focus=["endpoint mitigation", "air-quality monitoring"],
            )
        )

    if feasibility_score < 45 or score.readiness_score < 45:
        findings.append(
            DiagnosisFinding(
                code="monitoring_readiness_gap",
                title="Monitoring / Readiness Gap",
                severity="medium",
                summary="The corridor has signal worth tracking, but readiness is still too uncertain for a clear first capital intervention.",
                evidence={
                    "transition_feasibility": feasibility_score,
                    "readiness_score": score.readiness_score,
                },
                recommended_focus=["improved monitoring", "phased readiness assessment"],
            )
        )

    if not findings:
        findings.append(
            DiagnosisFinding(
                code="balanced_opportunity_profile",
                title="Balanced Opportunity Profile",
                severity="low",
                summary="No single bottleneck dominates the corridor, so the best move is to address the lowest readiness component first.",
                evidence={"readiness_score": score.readiness_score},
                recommended_focus=["targeted optimization"],
            )
        )

    findings.sort(key=lambda finding: {"high": 0, "medium": 1, "low": 2}[finding.severity])
    summary = findings[0].summary
    return DiagnosisPanel(corridor_id=corridor.corridor_id, summary=summary, findings=findings)
