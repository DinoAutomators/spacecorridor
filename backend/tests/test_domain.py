from __future__ import annotations

import csv
import os
import tempfile
import unittest

from backend.app.config import get_settings
from backend.app.data import load_data
from backend.app.diagnosis import diagnose_corridor
from backend.app.recommendation import recommend_for_corridor
from backend.app.scoring import score_corridor


class DomainLogicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.previous_data_path = os.environ.get("CORRIDORIQ_DATA_PATH")
        os.environ["CORRIDORIQ_DATA_PATH"] = self.temp_dir.name
        get_settings.cache_clear()
        load_data.cache_clear()
        self._write_fixture_data()
        data = load_data()
        self.corridors = {corridor.corridor_id: corridor for corridor in data.corridors}

    def tearDown(self) -> None:
        load_data.cache_clear()
        get_settings.cache_clear()
        if self.previous_data_path is None:
            os.environ.pop("CORRIDORIQ_DATA_PATH", None)
        else:
            os.environ["CORRIDORIQ_DATA_PATH"] = self.previous_data_path

    def _write_fixture_data(self) -> None:
        corridor_rows = [
            {
                "corridor_id": "pacific-gateway",
                "corridor_name": "Pacific Gateway",
                "start_port": "port_los_angeles",
                "end_port": "port_phoenix_inland",
                "region": "US Southwest",
                "mode": "maritime",
                "time_period": "2025",
                "description": "Fixture corridor for infrastructure testing.",
                "strategic_importance_note": "High-value freight lane.",
                "geometry": "[[-118.27,33.73],[-112.07,33.45]]",
                "no2_score": "74",
                "night_lights_score": "88",
                "shipping_emissions_score": "82",
                "port_readiness_score": "41",
                "connectivity_score": "52",
                "transition_feasibility_score": "58",
            },
            {
                "corridor_id": "gulf-heartland",
                "corridor_name": "Gulf Heartland",
                "start_port": "port_houston",
                "end_port": "port_dallas_inland",
                "region": "US South",
                "mode": "maritime",
                "time_period": "2025",
                "description": "Fixture corridor for connectivity testing.",
                "strategic_importance_note": "Strong freight value.",
                "geometry": "[[-95.24,29.73],[-96.8,32.78]]",
                "no2_score": "79",
                "night_lights_score": "71",
                "shipping_emissions_score": "85",
                "port_readiness_score": "63",
                "connectivity_score": "36",
                "transition_feasibility_score": "61",
            },
        ]
        port_rows = [
            {
                "port_id": "port_los_angeles",
                "port_name": "Port of Los Angeles",
                "country": "USA",
                "region": "California",
                "mode": "port",
                "lat": "33.73",
                "lon": "-118.27",
                "harbor_type": "Coastal",
                "cargo_capability": "true",
                "services_score": "92",
                "strategic_score": "95",
                "readiness_score": "43",
            },
            {
                "port_id": "port_phoenix_inland",
                "port_name": "Phoenix Inland Hub",
                "country": "USA",
                "region": "Arizona",
                "mode": "inland_hub",
                "lat": "33.45",
                "lon": "-112.07",
                "harbor_type": "Inland",
                "cargo_capability": "true",
                "services_score": "67",
                "strategic_score": "74",
                "readiness_score": "52",
            },
            {
                "port_id": "port_houston",
                "port_name": "Port of Houston",
                "country": "USA",
                "region": "Texas",
                "mode": "port",
                "lat": "29.73",
                "lon": "-95.24",
                "harbor_type": "Coastal",
                "cargo_capability": "true",
                "services_score": "84",
                "strategic_score": "88",
                "readiness_score": "63",
            },
            {
                "port_id": "port_dallas_inland",
                "port_name": "Dallas Inland Hub",
                "country": "USA",
                "region": "Texas",
                "mode": "inland_hub",
                "lat": "32.78",
                "lon": "-96.8",
                "harbor_type": "Inland",
                "cargo_capability": "true",
                "services_score": "62",
                "strategic_score": "72",
                "readiness_score": "38",
            },
        ]

        with open(os.path.join(self.temp_dir.name, "corridor_features.csv"), "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(corridor_rows[0].keys()))
            writer.writeheader()
            writer.writerows(corridor_rows)

        with open(os.path.join(self.temp_dir.name, "port_features.csv"), "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(port_rows[0].keys()))
            writer.writeheader()
            writer.writerows(port_rows)

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
