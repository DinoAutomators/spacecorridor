from __future__ import annotations

from fastapi import HTTPException

from .data import load_data
from .diagnosis import diagnose_corridor
from .recommendation import recommend_for_corridor
from .schemas import (
    Coordinate,
    CorridorDetailView,
    CorridorMapCard,
    CorridorMetrics,
    CorridorRecord,
    PortRecord,
)
from .scoring import score_corridor


class CorridorService:
    def __init__(self) -> None:
        self.data = load_data()
        self._ports_by_id = {port.port_id: port for port in self.data.ports}
        self._ports_by_name = {port.port_name.lower(): port for port in self.data.ports}

    def list_corridors(self) -> list[CorridorRecord]:
        return sorted(self.data.corridors, key=lambda corridor: corridor.corridor_name)

    def get_corridor(self, corridor_id: str) -> CorridorRecord:
        corridor = next((item for item in self.data.corridors if item.corridor_id == corridor_id), None)
        if corridor is None:
            raise HTTPException(status_code=404, detail=f"Corridor '{corridor_id}' not found.")
        return corridor

    def _resolve_port(self, reference: str) -> PortRecord | None:
        port = self._ports_by_id.get(reference)
        if port is not None:
            return port
        return self._ports_by_name.get(reference.lower())

    def _center_for(self, corridor: CorridorRecord) -> Coordinate:
        if corridor.center is not None:
            return corridor.center
        if corridor.geometry:
            first = corridor.geometry[0]
            last = corridor.geometry[-1]
            return Coordinate(
                lat=round((float(first[1]) + float(last[1])) / 2, 4),
                lon=round((float(first[0]) + float(last[0])) / 2, 4),
            )
        related_ports = [self._resolve_port(corridor.start_port), self._resolve_port(corridor.end_port)]
        valid_ports = [port for port in related_ports if port is not None]
        if valid_ports:
            return Coordinate(
                lat=round(sum(port.lat for port in valid_ports) / len(valid_ports), 4),
                lon=round(sum(port.lon for port in valid_ports) / len(valid_ports), 4),
            )
        return Coordinate(lat=0.0, lon=0.0)

    def list_ports(self, corridor_id: str | None = None) -> list[PortRecord]:
        ports = self.data.ports
        if corridor_id is not None:
            corridor = self.get_corridor(corridor_id)
            port_refs = {corridor.start_port, corridor.end_port}
            ports = [port for port in ports if port.port_id in port_refs or port.port_name in port_refs]
        return sorted(ports, key=lambda port: port.port_name)

    def metrics_for(self, corridor: CorridorRecord) -> CorridorMetrics:
        return CorridorMetrics(
            no2_score=corridor.no2_score,
            night_lights_score=corridor.night_lights_score,
            shipping_emissions_score=corridor.shipping_emissions_score,
            port_readiness_score=corridor.port_readiness_score,
            connectivity_score=corridor.connectivity_score,
            transition_feasibility_score=corridor.transition_feasibility_score,
        )

    def map_card_for(self, corridor_id: str) -> CorridorMapCard:
        corridor = self.get_corridor(corridor_id)
        score = score_corridor(corridor)
        diagnosis = diagnose_corridor(corridor)
        recommendation = recommend_for_corridor(corridor)
        return CorridorMapCard(
            corridor_id=corridor.corridor_id,
            corridor_name=corridor.corridor_name,
            start_port=corridor.start_port,
            end_port=corridor.end_port,
            readiness_score=score.readiness_score,
            no2_score=corridor.no2_score,
            night_lights_score=corridor.night_lights_score,
            band=score.band,
            bottleneck_label=diagnosis.findings[0].title,
            top_recommendation=recommendation.recommendations[0].title,
            center=self._center_for(corridor),
        )

    def detail_view_for(self, corridor_id: str) -> CorridorDetailView:
        corridor = self.get_corridor(corridor_id)
        return CorridorDetailView(
            corridor=corridor,
            ports=self.list_ports(corridor.corridor_id),
            metrics=self.metrics_for(corridor),
            score=score_corridor(corridor),
            diagnosis_panel=diagnose_corridor(corridor),
            recommendation_panel=recommend_for_corridor(corridor),
            map_card=self.map_card_for(corridor.corridor_id),
        )
