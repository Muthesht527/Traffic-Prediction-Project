"""Map a congestion score (0–100) to a hex colour and label for map rendering."""

from __future__ import annotations

from backend.config import COLOR_RANGES
from backend.utils.logger import get_logger

log = get_logger("colors")

_NO_COVERAGE_COLOR = "#9ca3af"  # grey
_NO_COVERAGE_LABEL = "Coverage Not Available"


def score_to_color(score: float | None) -> dict:
    """Return ``{"color": hex, "label": str}`` for the given score.

    ``score=None`` means the route is outside dataset coverage.
    """
    if score is None:
        return {"color": _NO_COVERAGE_COLOR, "label": _NO_COVERAGE_LABEL}

    for band in COLOR_RANGES:
        if band["min"] <= score <= band["max"]:
            return {"color": band["color"], "label": band["label"]}

    # Edge case — score slightly above 100 due to floating point
    if score > 100:
        return {"color": COLOR_RANGES[-1]["color"], "label": COLOR_RANGES[-1]["label"]}
    if score < 0:
        return {"color": COLOR_RANGES[0]["color"], "label": COLOR_RANGES[0]["label"]}

    return {"color": _NO_COVERAGE_COLOR, "label": _NO_COVERAGE_LABEL}


def segment_route_with_colors(
    coordinates: list[list[float]],
    score: float | None,
) -> list[dict]:
    """Split a route into segments each with a colour.

    Phase 1: the entire route gets a single score → single colour.  The
    interface returns a list of segments so that *future* phases can colour
    each segment independently without frontend changes.

    Each segment::

        {
            "coordinates": [[lng, lat], …],
            "color": "#ff0000",
            "congestion_score": 72.3,
            "label": "Heavy Congestion"
        }
    """
    if not coordinates:
        return []

    color_info = score_to_color(score)
    return [
        {
            "coordinates": coordinates,
            "color": color_info["color"],
            "congestion_score": score,
            "label": color_info["label"],
        }
    ]
