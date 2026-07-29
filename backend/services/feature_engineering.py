"""Feature engineering: converts user inputs + route + weather into the model feature vector.

The existing Random Forest was trained on 14 raw columns (including Timestamp,
Traffic_Condition as target).  At inference time we build a DataFrame with the
same columns so the preprocessor pipeline handles imputation / encoding
identically to training.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

from backend.config import DEFAULT_REGION
from backend.utils.logger import get_logger

log = get_logger("features")


def _approx_vehicle_count(distance_m: float, hour: int) -> int:
    """Estimate vehicle count based on distance and time-of-day."""
    import math

    base = max(30, distance_m / 50)  # ~1 vehicle per 50 m
    # Peak hours boost (8-10 AM, 5-8 PM)
    if 8 <= hour <= 10 or 17 <= hour <= 20:
        base *= 1.8
    elif 0 <= hour <= 5:
        base *= 0.4
    return int(min(base, 500))


def _approx_traffic_speed(hour: int, rain_1h: float) -> float:
    """Estimate average traffic speed (km/h) given hour and rain."""
    import math

    base = 35.0
    # Night: faster
    if 0 <= hour <= 5:
        base = 50.0
    # Peak: slower
    elif 8 <= hour <= 10:
        base = 22.0
    elif 17 <= hour <= 20:
        base = 20.0
    # Rain reduces speed
    if rain_1h > 0.5:
        base *= 0.75
    return round(base + 3 * math.sin(hour), 1)


def _approx_road_occupancy(vehicle_count: int, hour: int) -> float:
    """Estimate road occupancy percentage."""
    base = min(95.0, vehicle_count / 5.0)
    return round(base, 1)


def _estimate_traffic_light_state(hour: int, rng_seed: float) -> str:
    """Approximate most likely traffic light state at an intersection."""
    import math

    # Deterministic pseudo-random based on seed
    val = abs(math.sin(rng_seed * 1000))
    if hour in (0, 1, 2, 3, 4, 23):
        if val < 0.6:
            return "Green"
        elif val < 0.85:
            return "Yellow"
        else:
            return "Red"
    else:
        if val < 0.4:
            return "Green"
        elif val < 0.65:
            return "Red"
        else:
            return "Yellow"


def _estimate_weather_condition(rain_1h: float, wind_speed: float) -> str:
    """Map rain and wind to a weather condition string matching training labels."""
    if rain_1h > 2.0:
        return "Rain"
    if rain_1h > 0.5:
        return "Rain"
    if wind_speed > 15:
        return "Cloudy"
    if rain_1h > 0.1:
        return "Fog"
    return "Clear"


def build_features(
    origin: tuple[float, float],
    destination: tuple[float, float],
    target_dt: datetime,
    route: dict,
    weather: dict,
) -> pd.DataFrame:
    """Build the feature DataFrame that the model preprocessor expects.

    Returns a single-row DataFrame with the same raw columns used during
    training (minus the target).
    """
    distance_m = route.get("distance_m", 5000)
    lat = (origin[0] + destination[0]) / 2
    lng = (origin[1] + destination[1]) / 2
    hour = target_dt.hour

    rain_1h = weather.get("rain_1h", 0.0)
    wind_speed = weather.get("wind_speed", 5.0)
    temperature = weather.get("temperature", 30.0)
    humidity = weather.get("humidity", 70.0)

    vehicle_count = _approx_vehicle_count(distance_m, hour)
    speed = _approx_traffic_speed(hour, rain_1h)
    occupancy = _approx_road_occupancy(vehicle_count, hour)

    seed = lat + lng + hour * 0.01
    light_state = _estimate_traffic_light_state(hour, seed)
    weather_cond = _estimate_weather_condition(rain_1h, wind_speed)

    # Accident probability (low by default, higher during rain + peak)
    accident = 1 if (rain_1h > 1.0 and 8 <= hour <= 10) else 0

    # Sentiment score derived from congestion heuristics
    import math
    sentiment = round(-0.3 + 0.6 * math.cos(hour * math.pi / 12) - rain_1h * 0.1, 2)
    sentiment = max(-1.0, min(1.0, sentiment))

    # Ride-sharing demand
    ride_demand = int(vehicle_count * 0.2 + 10 * (1 if 8 <= hour <= 20 else 0))
    ride_demand = min(ride_demand, 100)

    # Parking availability (inversely related to vehicle count)
    parking = max(0, 60 - int(vehicle_count / 4))

    # Emission levels correlate with congestion
    emission = round(180 + vehicle_count * 0.8 + (10 if rain_1h > 0 else 0), 1)

    # Energy consumption
    energy = round(6 + vehicle_count * 0.03 + (3 if rain_1h > 0 else 0), 1)

    timestamp_str = target_dt.strftime("%d-%m-%Y %H:%M")

    row = {
        "Timestamp": timestamp_str,
        "Latitude": lat,
        "Longitude": lng,
        "Vehicle_Count": vehicle_count,
        "Traffic_Speed_kmh": speed,
        "Road_Occupancy_%": occupancy,
        "Traffic_Light_State": light_state,
        "Weather_Condition": weather_cond,
        "Accident_Report": accident,
        "Sentiment_Score": sentiment,
        "Ride_Sharing_Demand": ride_demand,
        "Parking_Availability": parking,
        "Emission_Levels_g_km": emission,
        "Energy_Consumption_L_h": energy,
    }
    log.info("Feature row: %s", row)
    return pd.DataFrame([row])
