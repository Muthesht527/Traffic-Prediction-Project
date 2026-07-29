"""Geocoding via the Nominatim (OpenStreetMap) service."""

from __future__ import annotations

import requests

from backend.config import NOMINATIM_BASE_URL
from backend.utils.logger import get_logger

log = get_logger("geocoding")

_HEADERS = {"User-Agent": "TrafficForecastApp/1.0 (hackathon-demo)"}


def geocode(query: str) -> dict | None:
    """Return ``{"lat": float, "lng": float, "display_name": str}`` or *None*."""
    try:
        resp = requests.get(
            f"{NOMINATIM_BASE_URL}/search",
            params={"q": query, "format": "json", "limit": 1},
            headers=_HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        item = data[0]
        return {
            "lat": float(item["lat"]),
            "lng": float(item["lon"]),
            "display_name": item.get("display_name", query),
        }
    except Exception as exc:
        log.warning("Geocoding failed for %r: %s", query, exc)
        return None


def reverse_geocode(lat: float, lng: float) -> dict | None:
    """Return ``{"lat", "lng", "display_name"}`` or *None*."""
    try:
        resp = requests.get(
            f"{NOMINATIM_BASE_URL}/reverse",
            params={"lat": lat, "lon": lng, "format": "json"},
            headers=_HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        item = resp.json()
        return {
            "lat": lat,
            "lng": lng,
            "display_name": item.get("display_name", f"{lat}, {lng}"),
        }
    except Exception as exc:
        log.warning("Reverse geocoding failed for (%s, %s): %s", lat, lng, exc)
        return None
