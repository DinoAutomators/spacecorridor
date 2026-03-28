from __future__ import annotations

from fastapi import HTTPException

from .data import load_data
from .diagnosis import diagnose_corridor
from .recommendation import recommend_for_corridor
from .schemas import (
    CorridorDetailView,
    CorridorMapCard,
    CorridorRecord,
    PortRecord,
)
from .scoring import score_corridor


class CorridorService:
    def __init__(self) -> None:
        self.data = load_data()

    def list_corridors(self) -> list[CorridorRecord]:
        return sorted(self.data.corridors, key=lambda corridor: corridor.name)

    def get_corridor(self, corridor_id: str) -> CorridorRecord:
        corridor = next((item for item in self.data.corridors if item.id == corridor_id), None)
        if corridor is None:
            raise HTTPException(status_code=404, detail=f"Corridor '{corridor_id}' not found.")
        return corridor

    def list_ports(self, corridor_id: str | None = None) -> list[PortRecord]:
        ports = self.data.ports
        if corridor_id is not None:
            ports = [port for port in ports if port.corridor_id == corridor_id]
        return sorted(ports, key=lambda port: port.name)

    def map_card_for(self, corridor_id: str) -> CorridorMapCard:
        corridor = self.get_corridor(corridor_id)
        score = score_corridor(corridor)
        diagnosis = diagnose_corridor(corridor)
        recommendation = recommend_for_corridor(corridor)
        return CorridorMapCard(
            corridor_id=corridor.id,
            corridor_name=corridor.name,
            origin=corridor.origin,
            destination=corridor.destination,
            score=score.overall_score,
            band=score.band,
            top_diagnosis=diagnosis.findings[0].title,
            top_recommendation=recommendation.recommendations[0].title,
            center=corridor.center,
        )

    def detail_view_for(self, corridor_id: str) -> CorridorDetailView:
        corridor = self.get_corridor(corridor_id)
        return CorridorDetailView(
            corridor=corridor,
            ports=self.list_ports(corridor.id),
            score=score_corridor(corridor),
            diagnosis_panel=diagnose_corridor(corridor),
            recommendation_panel=recommend_for_corridor(corridor),
            map_card=self.map_card_for(corridor.id),
        )

