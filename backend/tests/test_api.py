from __future__ import annotations

import importlib
import unittest

from fastapi.testclient import TestClient

from backend.tests.helpers import BackendFixtureMixin


class APITests(BackendFixtureMixin, unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        import backend.app.main as main_module

        importlib.reload(main_module)
        self.client = TestClient(main_module.app)

    def test_corridor_detail_returns_ai_fields(self) -> None:
        response = self.client.get("/corridors/pacific-gateway")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("ai_explanation", payload)
        self.assertIn("ai_explanations", payload)
        self.assertEqual(payload["ai_explanations"]["selected_variant_id"], "analyst")

    def test_corridor_detail_can_select_variant(self) -> None:
        response = self.client.get("/corridors/pacific-gateway?explanation_variant=executive")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["ai_explanations"]["selected_variant_id"], "executive")
        executive_text = next(
            variant["full_explanation"]
            for variant in payload["ai_explanations"]["variants"]
            if variant["id"] == "executive"
        )
        self.assertEqual(payload["ai_explanation"], executive_text)

    def test_corridors_list_stays_lightweight(self) -> None:
        response = self.client.get("/corridors")
        self.assertEqual(response.status_code, 200)
        first_item = response.json()["items"][0]
        self.assertNotIn("ai_explanation", first_item)
