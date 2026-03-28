from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, computed_field, field_validator


class Coordinate(BaseModel):
    lat: float
    lon: float


class CorridorFeatures(BaseModel):
    emissions_intensity_index: float = Field(ge=0, le=100)
    pollution_burden_index: float = Field(ge=0, le=100)
    freight_volume_index: float = Field(ge=0, le=100)
    throughput_index: float = Field(ge=0, le=100)
    port_capacity_index: float = Field(ge=0, le=100)
    port_electrification_index: float = Field(ge=0, le=100)
    low_carbon_fuel_index: float = Field(ge=0, le=100)
    rail_connectivity_index: float = Field(ge=0, le=100)
    inland_ev_support_index: float = Field(ge=0, le=100)
    cross_mode_coordination_index: float = Field(ge=0, le=100)
    policy_support_index: float = Field(ge=0, le=100)
    permitting_readiness_index: float = Field(ge=0, le=100)
    land_availability_index: float = Field(ge=0, le=100)
    workforce_readiness_index: float = Field(ge=0, le=100)


class PortRecord(BaseModel):
    id: str
    corridor_id: str
    name: str
    country: str
    state_or_region: str
    mode: str = "port"
    center: Coordinate
    throughput_index: float = Field(ge=0, le=100)
    electrification_readiness_index: float = Field(ge=0, le=100)
    low_carbon_fuel_readiness_index: float = Field(ge=0, le=100)
    intermodal_access_index: float = Field(ge=0, le=100)


class CorridorRecord(BaseModel):
    id: str
    name: str
    origin: str
    destination: str
    region: str
    description: str
    center: Coordinate
    tags: list[str] = Field(default_factory=list)
    feature_table: CorridorFeatures


class DataBundle(BaseModel):
    corridors: list[CorridorRecord]
    ports: list[PortRecord]


class ScoreComponent(BaseModel):
    key: str
    label: str
    score: float
    weight: float
    metrics: dict[str, float]
    rationale: str


class CorridorScore(BaseModel):
    corridor_id: str
    overall_score: float
    band: Literal["leading", "ready", "emerging", "constrained"]
    components: list[ScoreComponent]
    strengths: list[str]
    shortfalls: list[str]


class DiagnosisFinding(BaseModel):
    code: str
    title: str
    severity: Literal["high", "medium", "low"]
    summary: str
    evidence: dict[str, float]
    recommended_focus: list[str]


class DiagnosisPanel(BaseModel):
    corridor_id: str
    summary: str
    findings: list[DiagnosisFinding]


class RecommendationItem(BaseModel):
    code: str
    title: str
    priority: Literal["high", "medium", "low"]
    summary: str
    rationale: str
    triggered_by: list[str]
    target_metrics: list[str]


class RecommendationPanel(BaseModel):
    corridor_id: str
    summary: str
    recommendations: list[RecommendationItem]


class CorridorMapCard(BaseModel):
    corridor_id: str
    corridor_name: str
    origin: str
    destination: str
    score: float
    band: str
    top_diagnosis: str
    top_recommendation: str
    center: Coordinate


class CorridorDetailView(BaseModel):
    corridor: CorridorRecord
    ports: list[PortRecord]
    score: CorridorScore
    diagnosis_panel: DiagnosisPanel
    recommendation_panel: RecommendationPanel
    map_card: CorridorMapCard


class CorridorListResponse(BaseModel):
    count: int
    items: list[CorridorMapCard]


class PortListResponse(BaseModel):
    count: int
    items: list[PortRecord]


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str


class PortsQuery(BaseModel):
    corridor_id: str | None = None

    @field_validator("corridor_id")
    @classmethod
    def empty_string_to_none(cls, value: str | None) -> str | None:
        if value == "":
            return None
        return value

    @computed_field
    @property
    def has_filter(self) -> bool:
        return self.corridor_id is not None

