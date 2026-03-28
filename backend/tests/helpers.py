from __future__ import annotations

import csv
import os
import tempfile

from backend.app.config import get_settings
from backend.app.data import load_data
from backend.app.explanations import clear_explanation_cache


class BackendFixtureMixin:
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.previous_env = {
            "CORRIDORIQ_DATA_PATH": os.environ.get("CORRIDORIQ_DATA_PATH"),
            "CORRIDORIQ_AI_ENABLED": os.environ.get("CORRIDORIQ_AI_ENABLED"),
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
            "OPENAI_MODEL": os.environ.get("OPENAI_MODEL"),
            "CORRIDORIQ_AI_TIMEOUT_SECONDS": os.environ.get("CORRIDORIQ_AI_TIMEOUT_SECONDS"),
            "CORRIDORIQ_AI_VARIANT_COUNT": os.environ.get("CORRIDORIQ_AI_VARIANT_COUNT"),
            "CORRIDORIQ_AI_PROMPT_VERSION": os.environ.get("CORRIDORIQ_AI_PROMPT_VERSION"),
        }
        os.environ["CORRIDORIQ_DATA_PATH"] = self.temp_dir.name
        os.environ["CORRIDORIQ_AI_ENABLED"] = "false"
        get_settings.cache_clear()
        load_data.cache_clear()
        clear_explanation_cache()
        self._write_fixture_data()

    def tearDown(self) -> None:
        load_data.cache_clear()
        get_settings.cache_clear()
        clear_explanation_cache()
        for key, value in self.previous_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

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
