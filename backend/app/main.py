from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .schemas import (
    CorridorDetailView,
    CorridorListResponse,
    CorridorScore,
    DiagnosisPanel,
    HealthResponse,
    PortListResponse,
    RecommendationPanel,
)
from .service import CorridorService

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend service for CorridorIQ scoring, diagnosis, and recommendations.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = CorridorService()


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", app=settings.app_name, version=settings.app_version)


@app.get("/corridors", response_model=CorridorListResponse, tags=["corridors"])
def list_corridors() -> CorridorListResponse:
    items = [service.map_card_for(corridor.id) for corridor in service.list_corridors()]
    return CorridorListResponse(count=len(items), items=items)


@app.get("/corridors/{corridor_id}", response_model=CorridorDetailView, tags=["corridors"])
def corridor_detail(corridor_id: str) -> CorridorDetailView:
    return service.detail_view_for(corridor_id)


@app.get("/ports", response_model=PortListResponse, tags=["ports"])
def list_ports(corridor_id: str | None = Query(default=None)) -> PortListResponse:
    items = service.list_ports(corridor_id=corridor_id)
    return PortListResponse(count=len(items), items=items)


@app.get("/score/{corridor_id}", response_model=CorridorScore, tags=["analysis"])
def corridor_score(corridor_id: str) -> CorridorScore:
    corridor = service.get_corridor(corridor_id)
    return service.detail_view_for(corridor.id).score


@app.get("/diagnosis/{corridor_id}", response_model=DiagnosisPanel, tags=["analysis"])
def corridor_diagnosis(corridor_id: str) -> DiagnosisPanel:
    corridor = service.get_corridor(corridor_id)
    return service.detail_view_for(corridor.id).diagnosis_panel


@app.get("/recommendation/{corridor_id}", response_model=RecommendationPanel, tags=["analysis"])
def corridor_recommendation(corridor_id: str) -> RecommendationPanel:
    corridor = service.get_corridor(corridor_id)
    return service.detail_view_for(corridor.id).recommendation_panel
