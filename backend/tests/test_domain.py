from __future__ import annotations

import unittest

from backend.app.data import load_data
from backend.app.diagnosis import diagnose_corridor
from backend.app.recommendation import recommend_for_corridor
from backend.app.scoring import score_corridor


class DomainLogicTests(unittest.TestCase):
    def setUp(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
