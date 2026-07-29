"""SQLite database service for storing prediction history and caching.

Phase 1 uses a lightweight SQLite store so the demo has zero external
dependencies.  The service exposes a simple API that future phases can
extend (PostgreSQL, Redis, etc.) without changing callers.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

from backend.config import PROJECT_ROOT
from backend.utils.logger import get_logger

log = get_logger("database")

_DB_PATH = PROJECT_ROOT / "data" / "traffic_forecast.db"

_local = threading.local()


def _get_connection() -> sqlite3.Connection:
    """Return a thread-local database connection."""
    if not hasattr(_local, "connection") or _local.connection is None:
        _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        _local.connection = sqlite3.connect(str(_DB_PATH))
        _local.connection.row_factory = sqlite3.Row
        _local.connection.execute("PRAGMA journal_mode=WAL")
    return _local.connection


def init_db() -> None:
    """Create tables if they do not exist."""
    conn = _get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            source_lat REAL,
            source_lng REAL,
            source_label TEXT,
            destination_lat REAL,
            destination_lng REAL,
            destination_label TEXT,
            target_datetime TEXT,
            congestion_score REAL,
            predicted_condition TEXT,
            class_probabilities TEXT,
            distance_m REAL,
            duration_s REAL,
            weather_temperature REAL,
            weather_humidity REAL,
            weather_rain REAL,
            weather_wind REAL,
            in_coverage INTEGER,
            route_source TEXT,
            raw_request TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_prediction_created
            ON prediction_history (created_at);
        """
    )
    conn.commit()
    log.info("Database initialised at %s", _DB_PATH)


# ── CRUD ──────────────────────────────────────────────────────────────────

def save_prediction(payload: dict[str, Any]) -> int:
    """Insert a prediction record and return the row id."""
    conn = _get_connection()

    source = payload.get("source", {})
    destination = payload.get("destination", {})
    prediction = payload.get("prediction", {})
    route = payload.get("route", {})
    weather = payload.get("weather", {})
    coverage = payload.get("coverage", {})

    cursor = conn.execute(
        """
        INSERT INTO prediction_history (
            source_lat, source_lng, source_label,
            destination_lat, destination_lng, destination_label,
            target_datetime,
            congestion_score, predicted_condition, class_probabilities,
            distance_m, duration_s,
            weather_temperature, weather_humidity, weather_rain, weather_wind,
            in_coverage, route_source, raw_request
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            source.get("lat"),
            source.get("lng"),
            source.get("query"),
            destination.get("lat"),
            destination.get("lng"),
            destination.get("query"),
            payload.get("target_datetime"),
            prediction.get("congestion_score"),
            prediction.get("predicted_condition"),
            json.dumps(prediction.get("class_probabilities", {})),
            route.get("distance_m"),
            route.get("duration_s"),
            weather.get("temperature"),
            weather.get("humidity"),
            weather.get("rain_1h"),
            weather.get("wind_speed"),
            1 if coverage.get("available") else 0,
            route.get("source"),
            json.dumps(payload, default=str)[:10000],
        ),
    )
    conn.commit()
    row_id = cursor.lastrowid
    log.info("Prediction saved — id=%s", row_id)
    return row_id


def get_recent_predictions(limit: int = 20) -> list[dict]:
    """Return the most recent prediction records."""
    conn = _get_connection()
    rows = conn.execute(
        "SELECT * FROM prediction_history ORDER BY created_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def get_prediction_count() -> int:
    """Return total number of stored predictions."""
    conn = _get_connection()
    row = conn.execute("SELECT COUNT(*) AS cnt FROM prediction_history").fetchone()
    return row["cnt"]


def close() -> None:
    """Close the thread-local connection (if any)."""
    if hasattr(_local, "connection") and _local.connection is not None:
        _local.connection.close()
        _local.connection = None
