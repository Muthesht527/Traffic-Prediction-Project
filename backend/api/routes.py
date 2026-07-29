"""Flask API endpoints for the Traffic Forecast platform."""

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, jsonify, request

from backend.config import DEFAULT_REGION
from backend.services import (
    color_mapper,
    geocoding_service,
    prediction_service,
    route_service,
    weather_service,
)
from backend.utils.logger import get_logger

log = get_logger("api")

bp = Blueprint("api", __name__, url_prefix="/api")


# ── Health ──────────────────────────────────────────────────────────────

@bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


# ── Geocode ─────────────────────────────────────────────────────────────

@bp.get("/geocode")
def geocode():
    """Geocode a place name → lat/lng."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Missing 'q' parameter."}), 400
    result = geocoding_service.geocode(query)
    if result is None:
        return jsonify({"error": f"Could not geocode '{query}'."}), 404
    return jsonify(result), 200


# ── Coverage ────────────────────────────────────────────────────────────

@bp.get("/coverage")
def coverage():
    """Return the currently supported region."""
    return jsonify(DEFAULT_REGION), 200


@bp.get("/coverage/check")
def coverage_check():
    """Check whether a lat/lng falls inside dataset coverage."""
    try:
        lat = float(request.args["lat"])
        lng = float(request.args["lng"])
    except (KeyError, ValueError):
        return jsonify({"error": "Provide 'lat' and 'lng' query parameters."}), 400

    bounds = DEFAULT_REGION["bounds"]
    inside = (
        bounds["south"] <= lat <= bounds["north"]
        and bounds["west"] <= lng <= bounds["east"]
    )
    return jsonify({"lat": lat, "lng": lng, "in_coverage": inside}), 200


# ── Forecast ────────────────────────────────────────────────────────────

@bp.post("/forecast")
def forecast():
    """Main forecast endpoint.

    Expected JSON body::

        {
            "source": "Adyar, Chennai",       // or {"lat": …, "lng": …}
            "destination": "T. Nagar, Chennai",
            "date": "2024-03-15",
            "time": "08:30"
        }
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    # -- Resolve source ------------------------------------------------
    origin = _resolve_location(payload.get("source"))
    if origin is None:
        return jsonify({"error": "Invalid or missing 'source'."}), 400

    # -- Resolve destination -------------------------------------------
    destination = _resolve_location(payload.get("destination"))
    if destination is None:
        return jsonify({"error": "Invalid or missing 'destination'."}), 400

    # -- Parse date/time -----------------------------------------------
    target_dt = _parse_datetime(payload.get("date"), payload.get("time"))
    if target_dt is None:
        return jsonify({"error": "Invalid or missing 'date' / 'time'."}), 400

    # -- Coverage check ------------------------------------------------
    bounds = DEFAULT_REGION["bounds"]
    mid_lat = (origin[0] + destination[0]) / 2
    mid_lng = (origin[1] + destination[1]) / 2
    in_coverage = (
        bounds["south"] <= mid_lat <= bounds["north"]
        and bounds["west"] <= mid_lng <= bounds["east"]
    )

    # -- Get route -----------------------------------------------------
    route = route_service.get_route(origin, destination)
    if route is None:
        return jsonify({"error": "Could not retrieve route."}), 502

    # -- Get weather ---------------------------------------------------
    weather = weather_service.get_weather_forecast(mid_lat, mid_lng, target_dt)

    # -- Predict congestion --------------------------------------------
    if in_coverage:
        prediction = prediction_service.predict_congestion(
            origin, destination, target_dt, route, weather
        )
        congestion_score = prediction["congestion_score"]
    else:
        congestion_score = None
        prediction = {
            "congestion_score": None,
            "predicted_condition": None,
            "class_probabilities": {},
            "message": "Outside supported dataset coverage.",
        }

    # -- Colour segments -----------------------------------------------
    segments = color_mapper.segment_route_with_colors(
        route["coordinates"], congestion_score
    )

    # -- Build response ------------------------------------------------
    response = {
        "source": {
            "lat": origin[0],
            "lng": origin[1],
            "query": str(payload.get("source")),
        },
        "destination": {
            "lat": destination[0],
            "lng": destination[1],
            "query": str(payload.get("destination")),
        },
        "target_datetime": target_dt.isoformat(),
        "route": {
            "distance_m": route["distance_m"],
            "duration_s": route["duration_s"],
            "source": route["source"],
        },
        "weather": weather,
        "prediction": prediction,
        "segments": segments,
        "coverage": {"available": in_coverage, "region": DEFAULT_REGION["name"]},
    }
    return jsonify(response), 200


# ── helpers ────────────────────────────────────────────────────────────

def _resolve_location(value) -> tuple[float, float] | None:
    """Accept either ``{"lat": …, "lng": …}`` or a string place name."""
    if isinstance(value, dict):
        try:
            return (float(value["lat"]), float(value["lng"]))
        except (KeyError, TypeError, ValueError):
            return None
    if isinstance(value, str) and value.strip():
        result = geocoding_service.geocode(value.strip())
        if result:
            return (result["lat"], result["lng"])
    return None


def _parse_datetime(date_str, time_str) -> datetime | None:
    """Combine date + time strings into a datetime."""
    if not date_str or not time_str:
        return None
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return None
