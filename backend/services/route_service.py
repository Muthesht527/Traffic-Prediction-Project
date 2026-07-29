"""Routing via OpenRouteService (or OSRM fallback).

Returns the route geometry (list of [lng, lat] pairs) plus distance / duration.

When neither external service is reachable (e.g. offline development), a
straight-line synthetic route is returned so the rest of the pipeline
remains functional.
"""

from __future__ import annotations

import math

import requests

from backend.config import OPENROUTESERVICE_API_KEY, OPENROUTESERVICE_BASE_URL
from backend.utils.logger import get_logger

log = get_logger("route")

_PROFILE = "driving-car"


# ── helpers ───────────────────────────────────────────────────────────────

def _haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Approximate distance in metres between two points."""
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def _synthetic_route(start: tuple[float, float], end: tuple[float, float]) -> dict:
    """Generate a plausible straight-line route with intermediate points."""
    n_points = 20
    coords = []
    for i in range(n_points + 1):
        t = i / n_points
        lat = start[0] + t * (end[0] - start[0])
        lng = start[1] + t * (end[1] - start[1])
        # Add slight curvature
        offset = 0.001 * math.sin(t * math.pi)
        lat += offset
        lng += offset * 0.5
        coords.append([round(lng, 6), round(lat, 6)])  # [lng, lat]

    dist = _haversine_m(start[0], start[1], end[0], end[1])
    # Road distance is typically 1.2–1.4× straight-line
    road_dist = dist * 1.3
    # Assume avg 30 km/h in city
    duration = road_dist / (30_000 / 3600)

    return {
        "coordinates": coords,
        "distance_m": round(road_dist, 1),
        "duration_s": round(duration, 1),
        "source": "synthetic",
    }


def _ors_route(start: tuple[float, float], end: tuple[float, float]) -> dict | None:
    """Call OpenRouteService directions API."""
    if not OPENROUTESERVICE_API_KEY:
        return None
    url = f"{OPENROUTESERVICE_BASE_URL}/directions/{_PROFILE}"
    headers = {
        "Authorization": OPENROUTESERVICE_API_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "coordinates": [
            [start[1], start[0]],  # [lng, lat]
            [end[1], end[0]],
        ],
    }
    try:
        resp = requests.post(url, json=body, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        feature = data["routes"][0]
        coords = feature["geometry"]["coordinates"]  # [[lng, lat], …]
        summary = feature["summary"]
        return {
            "coordinates": coords,
            "distance_m": summary["distance"],
            "duration_s": summary["duration"],
            "source": "openrouteservice",
        }
    except Exception as exc:
        log.warning("OpenRouteService request failed: %s", exc)
        return None


def _osrm_route(start: tuple[float, float], end: tuple[float, float]) -> dict | None:
    """Free OSRM demo as fallback."""
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{start[1]},{start[0]};{end[1]},{end[0]}"
        f"?overview=full&geometries=geojson"
    )
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        route = data["routes"][0]
        coords = route["geometry"]["coordinates"]  # [[lng, lat], …]
        return {
            "coordinates": coords,
            "distance_m": route["distance"],
            "duration_s": route["duration"],
            "source": "osrm",
        }
    except Exception as exc:
        log.warning("OSRM request failed: %s", exc)
        return None


# ── public API ────────────────────────────────────────────────────────────

def get_route(
    origin: tuple[float, float],
    destination: tuple[float, float],
) -> dict | None:
    """Return route dict with ``coordinates`` ([lng, lat] pairs), ``distance_m``, ``duration_s``.

    Tries OpenRouteService → OSRM → synthetic route (guaranteed fallback).
    """
    result = _ors_route(origin, destination)
    if result is not None:
        return result
    log.info("Falling back to OSRM …")
    result = _osrm_route(origin, destination)
    if result is not None:
        return result
    log.info("External routing unavailable — using synthetic route.")
    return _synthetic_route(origin, destination)
