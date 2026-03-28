from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from threading import Lock
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pydantic import BaseModel, ValidationError

from .config import get_settings
from .schemas import (
    AIExplanationGenerationMetadata,
    AIExplanations,
    AIExplanationVariant,
    CorridorRecord,
    CorridorScore,
    DiagnosisPanel,
    PortRecord,
    RecommendationPanel,
)

VARIANT_DEFINITIONS: tuple[tuple[str, str], ...] = (
    ("concise", "Concise"),
    ("analyst", "Analyst"),
    ("executive", "Executive"),
)

_SYSTEM_PROMPT = """
You write grounded, credible corridor intelligence summaries for SpaceCorridor.

Rules:
- Use only the facts and labels provided in the input JSON.
- Do not invent metrics, ports, bottlenecks, recommendations, or policy claims.
- Keep the exact corridor name, readiness band, top bottleneck title, and top recommendation title aligned with the input.
- Produce variants with ids in this exact order: concise, analyst, executive.
- The concise variant should be compact and plain.
- The analyst variant should be detailed and evidence-led.
- The executive variant should be action-oriented and decision-friendly.
- Each full_explanation must read like a polished paragraph built from the three section fields.
- Return JSON only.
""".strip()

_CACHE: dict[tuple[str, str, str, str, int], AIExplanations] = {}
_CACHE_LOCK = Lock()


class _LLMExplanationPayload(BaseModel):
    selected_variant_id: str
    variants: list[AIExplanationVariant]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stable_json(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _component_snapshot(score: CorridorScore) -> list[dict]:
    return [
        {
            "key": component.key,
            "label": component.label,
            "score": component.score,
            "weight": component.weight,
            "metrics": component.metrics,
        }
        for component in score.components
    ]


def _build_prompt_input(
    corridor: CorridorRecord,
    ports: list[PortRecord],
    score: CorridorScore,
    diagnosis: DiagnosisPanel,
    recommendation: RecommendationPanel,
) -> dict:
    top_diagnosis = diagnosis.findings[0]
    top_recommendation = recommendation.recommendations[0]
    return {
        "corridor": {
            "corridor_id": corridor.corridor_id,
            "corridor_name": corridor.corridor_name,
            "start_port": corridor.start_port,
            "end_port": corridor.end_port,
            "region": corridor.region,
            "mode": corridor.mode,
            "time_period": corridor.time_period,
            "description": corridor.description,
            "strategic_importance_note": corridor.strategic_importance_note,
        },
        "ports": [
            {
                "port_id": port.port_id,
                "port_name": port.port_name,
                "country": port.country,
                "region": port.region,
                "mode": port.mode,
                "readiness_score": port.readiness_score,
                "strategic_score": port.strategic_score,
            }
            for port in ports
        ],
        "score": {
            "readiness_score": score.readiness_score,
            "band": score.band,
            "strengths": score.strengths,
            "shortfalls": score.shortfalls,
            "adjustments": score.adjustments,
            "components": _component_snapshot(score),
        },
        "diagnosis": {
            "summary": diagnosis.summary,
            "top_bottleneck": {
                "code": top_diagnosis.code,
                "title": top_diagnosis.title,
                "severity": top_diagnosis.severity,
                "summary": top_diagnosis.summary,
                "evidence": top_diagnosis.evidence,
                "recommended_focus": top_diagnosis.recommended_focus,
            },
        },
        "recommendation": {
            "summary": recommendation.summary,
            "top_recommendation": {
                "code": top_recommendation.code,
                "title": top_recommendation.title,
                "priority": top_recommendation.priority,
                "summary": top_recommendation.summary,
                "rationale": top_recommendation.rationale,
                "triggered_by": top_recommendation.triggered_by,
                "target_metrics": top_recommendation.target_metrics,
            },
        },
    }


def _quality_check(payload: _LLMExplanationPayload, prompt_input: dict, variant_count: int) -> bool:
    expected_ids = [item[0] for item in VARIANT_DEFINITIONS[:variant_count]]
    actual_ids = [variant.id for variant in payload.variants]
    if actual_ids != expected_ids:
        return False

    corridor_name = prompt_input["corridor"]["corridor_name"].lower()
    band = str(prompt_input["score"]["band"]).lower()
    bottleneck_title = prompt_input["diagnosis"]["top_bottleneck"]["title"].lower()
    recommendation_title = prompt_input["recommendation"]["top_recommendation"]["title"].lower()

    for variant in payload.variants:
        combined = " ".join(
            [
                variant.why_this_corridor_matters,
                variant.why_it_scored_this_way,
                variant.what_should_happen_next,
                variant.full_explanation,
            ]
        ).lower()
        if corridor_name not in combined:
            return False
        if band not in combined:
            return False
        if bottleneck_title not in combined:
            return False
        if recommendation_title not in combined:
            return False
    return True


def _default_selected_variant(variants: list[AIExplanationVariant], requested_variant: str | None) -> str:
    available = {variant.id for variant in variants}
    if requested_variant and requested_variant in available:
        return requested_variant
    if "analyst" in available:
        return "analyst"
    return variants[0].id


def _selected_explanation(explanations: AIExplanations) -> str:
    selected = next(
        variant.full_explanation
        for variant in explanations.variants
        if variant.id == explanations.selected_variant_id
    )
    return selected


def _make_full_explanation(variant: AIExplanationVariant) -> str:
    return " ".join(
        [
            variant.why_this_corridor_matters.strip(),
            variant.why_it_scored_this_way.strip(),
            variant.what_should_happen_next.strip(),
        ]
    ).strip()


def _top_component_labels(score: CorridorScore) -> tuple[str, str]:
    ranked = sorted(score.components, key=lambda component: component.score, reverse=True)
    strongest = ranked[0].label
    weakest = ranked[-1].label
    return strongest, weakest


def _fallback_variants(
    corridor: CorridorRecord,
    score: CorridorScore,
    diagnosis: DiagnosisPanel,
    recommendation: RecommendationPanel,
    variant_count: int,
) -> list[AIExplanationVariant]:
    strongest, weakest = _top_component_labels(score)
    top_diagnosis = diagnosis.findings[0]
    top_recommendation = recommendation.recommendations[0]
    readiness_score = f"{score.readiness_score:.1f}"
    variants: list[AIExplanationVariant] = []

    concise = AIExplanationVariant(
        id="concise",
        label="Concise",
        why_this_corridor_matters=(
            f"{corridor.corridor_name} matters because it links {corridor.start_port} and {corridor.end_port} "
            f"in a corridor with meaningful logistics and decarbonization relevance."
        ),
        why_it_scored_this_way=(
            f"It is currently rated {score.band} with a readiness score of {readiness_score}, driven most by "
            f"{strongest} and held back most by {weakest}. The main bottleneck is {top_diagnosis.title}."
        ),
        what_should_happen_next=(
            f"The first move should be {top_recommendation.title}, because {top_recommendation.rationale.lower()}"
        ),
        full_explanation="",
    )
    concise = concise.model_copy(update={"full_explanation": _make_full_explanation(concise)})
    variants.append(concise)

    analyst = AIExplanationVariant(
        id="analyst",
        label="Analyst",
        why_this_corridor_matters=(
            f"{corridor.corridor_name} stands out as a {corridor.region} corridor where actionability matters as much as "
            f"environmental pressure. It connects {corridor.start_port} to {corridor.end_port} and carries a profile that is "
            f"material enough to evaluate for near-term decarbonization intervention."
        ),
        why_it_scored_this_way=(
            f"The corridor lands in the {score.band} band at {readiness_score} because its strongest signal is {strongest}, "
            f"while {weakest} remains the limiting factor. The leading diagnosis is {top_diagnosis.title}, supported by "
            f"the current evidence in the rule-based scoring and diagnosis engine."
        ),
        what_should_happen_next=(
            f"The recommended next step is {top_recommendation.title}. That recommendation is prioritized because "
            f"{top_recommendation.rationale.lower()} This keeps the intervention aligned with the corridor's measured bottleneck."
        ),
        full_explanation="",
    )
    analyst = analyst.model_copy(update={"full_explanation": _make_full_explanation(analyst)})
    variants.append(analyst)

    executive = AIExplanationVariant(
        id="executive",
        label="Executive",
        why_this_corridor_matters=(
            f"{corridor.corridor_name} is worth attention because it combines a clear corridor role with measurable pressure "
            f"and a plausible intervention path."
        ),
        why_it_scored_this_way=(
            f"At {readiness_score} in the {score.band} band, the corridor is not being held back by lack of relevance; it is "
            f"being constrained mainly by {top_diagnosis.title}, with {weakest} as the key drag on readiness."
        ),
        what_should_happen_next=(
            f"Decision-makers should prioritize {top_recommendation.title} next, since {top_recommendation.rationale.lower()} "
            f"That is the most direct way to convert corridor potential into visible progress."
        ),
        full_explanation="",
    )
    executive = executive.model_copy(update={"full_explanation": _make_full_explanation(executive)})
    variants.append(executive)

    return variants[:variant_count]


def _fallback_explanations(
    corridor: CorridorRecord,
    score: CorridorScore,
    diagnosis: DiagnosisPanel,
    recommendation: RecommendationPanel,
    requested_variant: str | None,
    model_name: str,
) -> AIExplanations:
    settings = get_settings()
    variants = _fallback_variants(
        corridor=corridor,
        score=score,
        diagnosis=diagnosis,
        recommendation=recommendation,
        variant_count=settings.ai_variant_count,
    )
    selected_variant_id = _default_selected_variant(variants, requested_variant)
    return AIExplanations(
        selected_variant_id=selected_variant_id,
        variants=variants,
        generation_metadata=AIExplanationGenerationMetadata(
            model=model_name,
            prompt_version=settings.ai_prompt_version,
            generated_at=_utc_now_iso(),
            fallback_used=True,
        ),
    )


def _request_openai_structured_output(prompt_input: dict) -> _LLMExplanationPayload:
    settings = get_settings()
    response_schema = _LLMExplanationPayload.model_json_schema()
    body = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": _stable_json(prompt_input)},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "corridor_explanations",
                "strict": True,
                "schema": response_schema,
            },
        },
        "temperature": 0.2,
    }
    request = Request(
        url="https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=settings.ai_timeout_seconds) as response:
        raw_payload = json.loads(response.read().decode("utf-8"))

    message = raw_payload["choices"][0]["message"]
    content = message.get("content", "")
    if isinstance(content, list):
        text = "".join(part.get("text", "") for part in content if part.get("type") == "text")
    else:
        text = str(content)
    return _LLMExplanationPayload.model_validate_json(text)


def _generate_uncached(
    corridor: CorridorRecord,
    ports: list[PortRecord],
    score: CorridorScore,
    diagnosis: DiagnosisPanel,
    recommendation: RecommendationPanel,
    requested_variant: str | None,
) -> AIExplanations:
    settings = get_settings()
    prompt_input = _build_prompt_input(corridor, ports, score, diagnosis, recommendation)
    if not settings.ai_enabled or not settings.openai_api_key:
        return _fallback_explanations(
            corridor=corridor,
            score=score,
            diagnosis=diagnosis,
            recommendation=recommendation,
            requested_variant=requested_variant,
            model_name="deterministic-fallback",
        )

    try:
        llm_payload = _request_openai_structured_output(prompt_input)
        if not _quality_check(llm_payload, prompt_input, settings.ai_variant_count):
            raise ValueError("Generated explanations failed grounding checks.")
        selected_variant_id = _default_selected_variant(llm_payload.variants, requested_variant)
        return AIExplanations(
            selected_variant_id=selected_variant_id,
            variants=llm_payload.variants[: settings.ai_variant_count],
            generation_metadata=AIExplanationGenerationMetadata(
                model=settings.openai_model,
                prompt_version=settings.ai_prompt_version,
                generated_at=_utc_now_iso(),
                fallback_used=False,
            ),
        )
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, ValidationError, json.JSONDecodeError):
        return _fallback_explanations(
            corridor=corridor,
            score=score,
            diagnosis=diagnosis,
            recommendation=recommendation,
            requested_variant=requested_variant,
            model_name="deterministic-fallback",
        )


def _cache_key(prompt_input: dict) -> tuple[str, str, str, str, int]:
    settings = get_settings()
    payload_hash = hashlib.sha256(_stable_json(prompt_input).encode("utf-8")).hexdigest()
    return (
        prompt_input["corridor"]["corridor_id"],
        payload_hash,
        settings.ai_prompt_version,
        settings.openai_model,
        settings.ai_variant_count,
    )


def clear_explanation_cache() -> None:
    with _CACHE_LOCK:
        _CACHE.clear()


def generate_explanations_for_corridor(
    corridor: CorridorRecord,
    ports: list[PortRecord],
    score: CorridorScore,
    diagnosis: DiagnosisPanel,
    recommendation: RecommendationPanel,
    requested_variant: str | None = None,
) -> AIExplanations:
    prompt_input = _build_prompt_input(corridor, ports, score, diagnosis, recommendation)
    key = _cache_key(prompt_input)
    with _CACHE_LOCK:
        cached = _CACHE.get(key)

    if cached is None:
        cached = _generate_uncached(
            corridor=corridor,
            ports=ports,
            score=score,
            diagnosis=diagnosis,
            recommendation=recommendation,
            requested_variant=None,
        )
        with _CACHE_LOCK:
            _CACHE[key] = cached

    selected_variant_id = _default_selected_variant(cached.variants, requested_variant)
    return cached.model_copy(update={"selected_variant_id": selected_variant_id})


def selected_explanation_text(explanations: AIExplanations) -> str:
    return _selected_explanation(explanations)
