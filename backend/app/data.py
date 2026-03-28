from __future__ import annotations

import json
from functools import lru_cache

from .config import get_settings
from .schemas import DataBundle


def _read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_payload() -> dict:
    settings = get_settings()
    data_path = settings.data_path

    if data_path.is_dir():
        corridors_path = data_path / "corridors.json"
        ports_path = data_path / "ports.json"
        return {
            "corridors": _read_json(str(corridors_path)),
            "ports": _read_json(str(ports_path)),
        }

    return _read_json(str(data_path))


@lru_cache
def load_data() -> DataBundle:
    payload = _load_payload()
    return DataBundle.model_validate(payload)
