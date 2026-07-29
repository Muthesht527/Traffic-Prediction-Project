"""Application configuration loaded from environment variables with safe defaults."""

from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
MODEL_DIR = PROJECT_ROOT / "model"
DATASET_DIR = PROJECT_ROOT / "dataset"

MODEL_PATH = MODEL_DIR / "traffic_congestion_model.pkl"

# External API keys (set via environment variables)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OPENROUTESERVICE_API_KEY = os.getenv("OPENROUTESERVICE_API_KEY", "")

# API endpoints
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
OPENROUTESERVICE_BASE_URL = "https://api.openrouteservice.org/v2"
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org"

# Flask
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5001"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# CORS — allowed origins for /api/* (comma-separated), "*" = public access.
# Tighten this to your frontend origin (e.g. https://your-app.vercel.app)
# when the frontend calls the API directly instead of through a proxy.
_cors_raw = os.getenv("CORS_ORIGINS", "*")
CORS_ORIGINS = (
    "*"
    if _cors_raw.strip() == "*"
    else [o.strip() for o in _cors_raw.split(",") if o.strip()]
)

# Default supported region (Chennai, India) — only dataset coverage area
DEFAULT_REGION = {
    "name": "Chennai",
    "center": {"lat": 13.0827, "lng": 80.2707},
    "bounds": {
        "south": 12.90,
        "north": 13.25,
        "west": 80.05,
        "east": 80.35,
    },
}

# Congestion score → colour mapping
COLOR_RANGES = [
    {"min": 0, "max": 20, "color": "#22c55e", "label": "Low Congestion"},
    {"min": 21, "max": 40, "color": "#eab308", "label": "Light Congestion"},
    {"min": 41, "max": 70, "color": "#f97316", "label": "Moderate Congestion"},
    {"min": 71, "max": 100, "color": "#ef4444", "label": "Heavy Congestion"},
]
