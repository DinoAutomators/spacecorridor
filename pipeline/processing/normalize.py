from __future__ import annotations


def min_max_normalize(
    values: list[float],
    invert: bool = False,
    floor: float = 25.0,
    ceiling: float = 95.0,
) -> list[float]:
    """Normalize a list of floats to a bounded scale using min-max.

    With only 5 corridors, raw 0-100 min-max produces too-extreme
    spreads.  The floor/ceiling compress the range so no corridor
    scores an absolute zero on any metric.
    """
    if not values:
        return []
    lo = min(values)
    hi = max(values)
    if hi == lo:
        return [round((floor + ceiling) / 2.0, 2)] * len(values)
    span = ceiling - floor
    normalized = [floor + (v - lo) / (hi - lo) * span for v in values]
    if invert:
        normalized = [floor + ceiling - v for v in normalized]
    return [round(v, 2) for v in normalized]
