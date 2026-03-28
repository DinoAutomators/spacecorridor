from __future__ import annotations

import csv
import json
from functools import lru_cache
from pathlib import Path

from .config import get_settings
from .schemas import DataBundle


def _read_json(path: str) -> dict | list[dict]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _read_csv(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows: list[dict] = []
        for row in reader:
            normalized = {
                key: value if value != "" else None
                for key, value in row.items()
            }
            geometry = normalized.get("geometry")
            if isinstance(geometry, str):
                normalized["geometry"] = json.loads(geometry)
            rows.append(normalized)
        return rows


def _load_payload() -> dict:
    settings = get_settings()
    data_path = settings.data_path

    if not data_path.exists():
        return {"corridors": [], "ports": []}

    if data_path.is_dir():
        corridor_csv = data_path / "corridor_features.csv"
        port_csv = data_path / "port_features.csv"
        if corridor_csv.exists() and port_csv.exists():
            return {
                "corridors": _read_csv(str(corridor_csv)),
                "ports": _read_csv(str(port_csv)),
            }

        corridors_path = data_path / "corridors.json"
        ports_path = data_path / "ports.json"
        if corridors_path.exists() and ports_path.exists():
            return {
                "corridors": _read_json(str(corridors_path)),
                "ports": _read_json(str(ports_path)),
            }

        return {"corridors": [], "ports": []}

    if not data_path.is_file():
        return {"corridors": [], "ports": []}

    if Path(data_path).suffix.lower() == ".csv":
        return {"corridors": _read_csv(str(data_path)), "ports": []}

    if Path(data_path).suffix.lower() != ".json":
        return {"corridors": [], "ports": []}

    return _read_json(str(data_path))


@lru_cache
def load_data() -> DataBundle:
    payload = _load_payload()
    return DataBundle.model_validate(payload)
