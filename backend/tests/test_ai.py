from __future__ import annotations

import unittest
from unittest.mock import patch

from backend.app.data import load_data
from backend.app.diagnosis import diagnose_corridor
from backend.app import explanations as explanations_module
from backend.app.explanations import clear_explanation_cache, generate_explanations_for_corridor
from backend.app.recommendation import recommend_for_corridor
from backend.app.scoring import score_corridor
from backend.tests.helpers import BackendFixtureMixin


class AIExplanationTests(BackendFixtureMixin, unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        data = load_data()
        self.corridor = next(corridor for corridor in data.corridors if corridor.corridor_id == "pacific-gateway")
        self.ports = [port for port in data.ports if port.port_id in {"port_los_angeles", "port_phoenix_inland"}]
        self.score = score_corridor(self.corridor)
        self.diagnosis = diagnose_corridor(self.corridor)
        self.recommendation = recommend_for_corridor(self.corridor)

    def test_ai_disabled_returns_deterministic_fallback(self) -> None:
        explanations = generate_explanations_for_corridor(
            corridor=self.corridor,
            ports=self.ports,
            score=self.score,
            diagnosis=self.diagnosis,
            recommendation=self.recommendation,
        )
        self.assertTrue(explanations.generation_metadata.fallback_used)
        self.assertEqual(explanations.selected_variant_id, "analyst")
        self.assertEqual(len(explanations.variants), 3)
        self.assertIn("Pacific Gateway", explanations.variants[1].full_explanation)
        self.assertIn("Port Infrastructure Gap", explanations.variants[1].full_explanation)
        self.assertIn("Port electrification", explanations.variants[1].full_explanation)

    def test_requested_variant_changes_selected_output_without_regeneration(self) -> None:
        explanations = generate_explanations_for_corridor(
            corridor=self.corridor,
            ports=self.ports,
            score=self.score,
            diagnosis=self.diagnosis,
            recommendation=self.recommendation,
            requested_variant="executive",
        )
        self.assertEqual(explanations.selected_variant_id, "executive")
        self.assertEqual(len(explanations.variants), 3)

    def test_invalid_llm_payload_falls_back(self) -> None:
        with patch("backend.app.explanations._request_openai_structured_output", side_effect=ValueError("bad payload")):
            with patch("backend.app.explanations.get_settings") as mocked_settings:
                settings = mocked_settings.return_value
                settings.ai_enabled = True
                settings.openai_api_key = "test-key"
                settings.openai_model = "gpt-4o-mini"
                settings.ai_timeout_seconds = 5
                settings.ai_variant_count = 3
                settings.ai_prompt_version = "v1"
                explanations = generate_explanations_for_corridor(
                    corridor=self.corridor,
                    ports=self.ports,
                    score=self.score,
                    diagnosis=self.diagnosis,
                    recommendation=self.recommendation,
                )
        self.assertTrue(explanations.generation_metadata.fallback_used)
        self.assertEqual(explanations.generation_metadata.model, "deterministic-fallback")

    def test_valid_llm_payload_is_used_when_grounded(self) -> None:
        llm_payload = explanations_module._LLMExplanationPayload.model_validate(
            {
                "selected_variant_id": "analyst",
                "variants": [
                    {
                        "id": "concise",
                        "label": "Concise",
                        "why_this_corridor_matters": "Pacific Gateway matters because it is a high-relevance corridor in the emerging band with Port Infrastructure Gap as its main bottleneck.",
                        "why_it_scored_this_way": "Pacific Gateway is emerging because Port Infrastructure Gap remains the main drag, even though the readiness band and supporting metrics show material actionability.",
                        "what_should_happen_next": "Pacific Gateway should prioritize Port electrification next to address Port Infrastructure Gap in an emerging corridor.",
                        "full_explanation": "Pacific Gateway matters because it is a high-relevance corridor in the emerging band with Port Infrastructure Gap as its main bottleneck. Pacific Gateway is emerging because Port Infrastructure Gap remains the main drag, even though the readiness band and supporting metrics show material actionability. Pacific Gateway should prioritize Port electrification next to address Port Infrastructure Gap in an emerging corridor.",
                    },
                    {
                        "id": "analyst",
                        "label": "Analyst",
                        "why_this_corridor_matters": "Pacific Gateway is an emerging corridor whose relevance comes from linking key freight nodes while showing a clear Port Infrastructure Gap.",
                        "why_it_scored_this_way": "The Pacific Gateway corridor lands in the emerging band because Port Infrastructure Gap limits readiness even as measured activity and pressure justify action.",
                        "what_should_happen_next": "The highest-impact next step is Port electrification, which directly addresses the Port Infrastructure Gap identified for Pacific Gateway.",
                        "full_explanation": "Pacific Gateway is an emerging corridor whose relevance comes from linking key freight nodes while showing a clear Port Infrastructure Gap. The Pacific Gateway corridor lands in the emerging band because Port Infrastructure Gap limits readiness even as measured activity and pressure justify action. The highest-impact next step is Port electrification, which directly addresses the Port Infrastructure Gap identified for Pacific Gateway.",
                    },
                    {
                        "id": "executive",
                        "label": "Executive",
                        "why_this_corridor_matters": "Pacific Gateway is an emerging corridor with a visible Port Infrastructure Gap that creates a clear intervention target.",
                        "why_it_scored_this_way": "Its emerging position reflects real potential, but Port Infrastructure Gap still constrains performance.",
                        "what_should_happen_next": "Decision-makers should move on Port electrification first to close the Port Infrastructure Gap in Pacific Gateway.",
                        "full_explanation": "Pacific Gateway is an emerging corridor with a visible Port Infrastructure Gap that creates a clear intervention target. Its emerging position reflects real potential, but Port Infrastructure Gap still constrains performance. Decision-makers should move on Port electrification first to close the Port Infrastructure Gap in Pacific Gateway.",
                    },
                ],
            }
        )
        with patch("backend.app.explanations._request_openai_structured_output", return_value=llm_payload):
            with patch("backend.app.explanations.get_settings") as mocked_settings:
                settings = mocked_settings.return_value
                settings.ai_enabled = True
                settings.openai_api_key = "test-key"
                settings.openai_model = "gpt-4o-mini"
                settings.ai_timeout_seconds = 5
                settings.ai_variant_count = 3
                settings.ai_prompt_version = "v1"
                explanations = generate_explanations_for_corridor(
                    corridor=self.corridor,
                    ports=self.ports,
                    score=self.score,
                    diagnosis=self.diagnosis,
                    recommendation=self.recommendation,
                )
        self.assertFalse(explanations.generation_metadata.fallback_used)
        self.assertEqual(explanations.selected_variant_id, "analyst")

    def test_cache_hit_avoids_duplicate_model_calls(self) -> None:
        clear_explanation_cache()
        with patch("backend.app.explanations._request_openai_structured_output") as mocked_request:
            with patch("backend.app.explanations.get_settings") as mocked_settings:
                settings = mocked_settings.return_value
                settings.ai_enabled = True
                settings.openai_api_key = "test-key"
                settings.openai_model = "gpt-4o-mini"
                settings.ai_timeout_seconds = 5
                settings.ai_variant_count = 3
                settings.ai_prompt_version = "v1"
                mocked_request.return_value = {
                    "selected_variant_id": "analyst",
                    "variants": [],
                }
                mocked_request.side_effect = ValueError("invalid payload")
                generate_explanations_for_corridor(
                    corridor=self.corridor,
                    ports=self.ports,
                    score=self.score,
                    diagnosis=self.diagnosis,
                    recommendation=self.recommendation,
                )
                generate_explanations_for_corridor(
                    corridor=self.corridor,
                    ports=self.ports,
                    score=self.score,
                    diagnosis=self.diagnosis,
                    recommendation=self.recommendation,
                )
        self.assertEqual(mocked_request.call_count, 1)
