"""Configurable dataset column mapper.

Maps whatever column names the CSV uses to the canonical feature names the
pipeline expects.  This means swapping datasets or renaming columns never
breaks the model — just update the mapping.
"""

from __future__ import annotations

from typing import Any

from backend.utils.logger import get_logger

log = get_logger("column-mapper")

# ── Default mapping (Smart Mobility Dataset) ─────────────────────────────
# Canonical name  →  possible source column names (first match wins)
DEFAULT_COLUMN_MAP: dict[str, list[str]] = {
    "Timestamp": [
        "Timestamp", "timestamp", "datetime", "date_time", "time",
    ],
    "Latitude": [
        "Latitude", "latitude", "lat", "Lat",
    ],
    "Longitude": [
        "Longitude", "longitude", "lng", "lon", "Long",
    ],
    "Vehicle_Count": [
        "Vehicle_Count", "vehicle_count", "vehicles", "traffic_volume",
    ],
    "Traffic_Speed_kmh": [
        "Traffic_Speed_kmh", "traffic_speed", "speed_kmh", "avg_speed",
    ],
    "Road_Occupancy_%": [
        "Road_Occupancy_%", "road_occupancy", "occupancy_pct", "occupancy",
    ],
    "Traffic_Light_State": [
        "Traffic_Light_State", "traffic_light", "light_state", "signal",
    ],
    "Weather_Condition": [
        "Weather_Condition", "weather", "weather_condition", "conditions",
    ],
    "Accident_Report": [
        "Accident_Report", "accident", "accidents", "accident_report",
    ],
    "Sentiment_Score": [
        "Sentiment_Score", "sentiment", "sentiment_score",
    ],
    "Ride_Sharing_Demand": [
        "Ride_Sharing_Demand", "ride_sharing", "ride_demand",
    ],
    "Parking_Availability": [
        "Parking_Availability", "parking", "parking_availability",
    ],
    "Emission_Levels_g_km": [
        "Emission_Levels_g_km", "emissions", "emission_levels",
    ],
    "Energy_Consumption_L_h": [
        "Energy_Consumption_L_h", "energy_consumption", "fuel_consumption",
    ],
    "Traffic_Condition": [
        "Traffic_Condition", "traffic_condition", "congestion", "target",
    ],
}


def build_rename_map(
    df_columns: list[str],
    custom_map: dict[str, list[str]] | None = None,
) -> dict[str, str]:
    """Return ``{source_col: canonical_name}`` for columns present in *df_columns*.

    Raises ``ValueError`` if a required canonical column has no match.
    """
    mapping = custom_map or DEFAULT_COLUMN_MAP
    rename: dict[str, str] = {}
    df_col_set = set(df_columns)

    for canonical, candidates in mapping.items():
        for candidate in candidates:
            if candidate in df_col_set:
                rename[candidate] = canonical
                break

    # Validate required columns
    mapped_canonicals = set(rename.values())
    required = {"Timestamp", "Latitude", "Longitude", "Traffic_Condition"}
    missing = required - mapped_canonicals
    if missing:
        log.warning("Dataset missing columns for: %s", missing)

    log.info("Column mapping: %s", rename)
    return rename


def normalise_dataframe(df, custom_map=None):
    """Rename columns to canonical names and return the DataFrame."""
    rename = build_rename_map(list(df.columns), custom_map)
    return df.rename(columns=rename)
