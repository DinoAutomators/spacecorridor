from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, computed_field


class Coordinate(BaseModel):
    lat: float
    lon: float


class PortRecord(BaseModel):
    port_id: str
    port_name: str
    country: str
    region: str
    mode: str = "port"
    lat: float
    lon: float
    harbor_type: str | None = None
    cargo_capability: bool | None = None
    services_score: float | None = Field(default=None, ge=0, le=100)
    strategic_score: float | None = Field(default=None, ge=0, le=100)
    readiness_score: float | None = Field(default=None, ge=0, le=100)

    @computed_field
    @property
    def center(self) -> Coordinate:
        return Coordinate(lat=self.lat, lon=self.lon)


class CorridorRecord(BaseModel):
    corridor_id: str
    corridor_name: str
    start_port: str
    end_port: str
    region: str
    mode: str = "maritime"
    time_period: str = "latest available"
    description: str = ""
    strategic_importance_note: str = ""
    geometry: list[list[float]] = Field(default_factory=list)
    no2_score: float = Field(ge=0, le=100)
    night_lights_score: float = Field(ge=0, le=100)
    shipping_emissions_score: float = Field(ge=0, le=100)
    port_readiness_score: float = Field(ge=0, le=100)
    connectivity_score: float = Field(ge=0, le=100)
    transition_feasibility_score: float = Field(ge=0, le=100)
    center: Coordinate | None = None


class CorridorMetrics(BaseModel):
    no2_score: float
    night_lights_score: float
    shipping_emissions_score: float
    port_readiness_score: float
    connectivity_score: float
    transition_feasibility_score: float


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
    readiness_score: float
    band: Literal["leading", "ready", "emerging", "constrained"]
    components: list[ScoreComponent]
    strengths: list[str]
    shortfalls: list[str]
    adjustments: list[str]


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


class AIExplanationVariant(BaseModel):
    id: str
    label: str
    why_this_corridor_matters: str
    why_it_scored_this_way: str
    what_should_happen_next: str
    full_explanation: str


class AIExplanationGenerationMetadata(BaseModel):
    model: str
    prompt_version: str
    generated_at: str
    fallback_used: bool


class AIExplanations(BaseModel):
    selected_variant_id: str
    variants: list[AIExplanationVariant]
    generation_metadata: AIExplanationGenerationMetadata


class CorridorMapCard(BaseModel):
    corridor_id: str
    corridor_name: str
    start_port: str
    end_port: str
    readiness_score: float
    no2_score: float
    night_lights_score: float
    band: str
    bottleneck_label: str
    top_recommendation: str
    center: Coordinate


class CorridorDetailView(BaseModel):
    corridor: CorridorRecord
    ports: list[PortRecord]
    metrics: CorridorMetrics
    score: CorridorScore
    diagnosis_panel: DiagnosisPanel
    recommendation_panel: RecommendationPanel
    ai_explanation: str
    ai_explanations: AIExplanations
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
