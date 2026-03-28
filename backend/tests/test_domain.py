from __future__ import annotations

import os
import unittest

from backend.app.config import get_settings
from backend.app.data import load_data
from backend.app.diagnosis import diagnose_corridor
from backend.app.recommendation import recommend_for_corridor
from backend.app.scoring import score_corridor
from backend.tests.helpers import BackendFixtureMixin


class DomainLogicTests(BackendFixtureMixin, unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        data = load_data()
        self.corridors = {corridor.corridor_id: corridor for corridor in data.corridors}

    def test_scoring_returns_weighted_components(self) -> None:
        score = score_corridor(self.corridors["pacific-gateway"])
        self.assertEqual(len(score.components), 5)
        self.assertGreater(score.readiness_score, 0)
        self.assertEqual(score.band, "emerging")

    def test_diagnosis_finds_infrastructure_bottleneck(self) -> None:
        diagnosis = diagnose_corridor(self.corridors["pacific-gateway"])
        finding_codes = {finding.code for finding in diagnosis.findings}
        self.assertIn("port_infrastructure_gap", finding_codes)

    def test_recommendations_include_ev_support_for_connectivity_gap(self) -> None:
        recommendation = recommend_for_corridor(self.corridors["gulf-heartland"])
        recommendation_codes = {item.code for item in recommendation.recommendations}
        self.assertIn("inland_ev_truck_support", recommendation_codes)

    def test_missing_data_path_returns_empty_bundle(self) -> None:
        os.environ["CORRIDORIQ_DATA_PATH"] = os.path.join(self.temp_dir.name, "missing")
        load_data.cache_clear()
        get_settings.cache_clear()
        data = load_data()
        self.assertEqual(data.corridors, [])
        self.assertEqual(data.ports, [])


if __name__ == "__main__":
    unittest.main()
