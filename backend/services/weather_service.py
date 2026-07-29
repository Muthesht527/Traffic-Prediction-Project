"""Weather forecast via the OpenWeather API.

Falls back to a plausible synthetic forecast when no API key is configured
so that the demo remains functional during hackathon development.
"""

from __future__ import annotations

from datetime import datetime

import requests

from backend.config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL
from backend.utils.logger import get_logger

log = get_logger("weather")


def _synthetic_forecast(lat: float, lng: float, dt: datetime) -> dict:
    """Return a plausible mock forecast when the API key is absent."""
    import math

    hour = dt.hour
    # Temperature varies with hour (cooler at night)
    temperature = 28 + 6 * math.sin((hour - 6) * math.pi / 12)
    humidity = 70 + 15 * math.cos((hour - 14) * math.pi / 12)
    wind_speed = 8 + 4 * math.sin(hour * math.pi / 8)
    # Rain probability based on latitude (coastal Chennai pattern)
    rain_1h = 0.0 if (hour % 3 != 0) else round(1.2 * abs(math.sin(lat)), 1)

    return {
        "temperature": round(temperature, 1),
        "humidity": round(humidity, 1),
        "wind_speed": round(wind_speed, 1),
        "rain_1h": rain_1h,
        "weather_description": "rain" if rain_1h > 0.5 else "clear",
        "source": "synthetic",
    }


def get_weather_forecast(lat: float, lng: float, target_dt: datetime) -> dict:
    """Return a weather dict for the given location and target datetime.

    Keys: ``temperature`` (°C), ``humidity`` (%), ``wind_speed`` (m/s),
    ``rain_1h`` (mm), ``weather_description``, ``source``.
    """
    if not OPENWEATHER_API_KEY:
        log.info("No OpenWeather API key — returning synthetic forecast.")
        return _synthetic_forecast(lat, lng, target_dt)

    try:
        # Use the One-Call API 3.0 for daily forecast
        url = f"{OPENWEATHER_BASE_URL}/forecast"
        params = {
            "lat": lat,
            "lon": lng,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Find the closest forecast entry to target_dt
        target_ts = target_dt.timestamp()
        closest = min(data["list"], key=lambda x: abs(x["dt"] - target_ts))
        main = closest["main"]
        wind = closest.get("wind", {})
        rain = closest.get("rain", {})
        desc = closest["weather"][0]["description"]

        return {
            "temperature": main.get("temp", 30),
            "humidity": main.get("humidity", 70),
            "wind_speed": wind.get("speed", 5),
            "rain_1h": rain.get("1h", 0.0),
            "weather_description": desc,
            "source": "openweathermap",
        }
    except Exception as exc:
        log.warning("OpenWeather request failed: %s — falling back to synthetic.", exc)
        return _synthetic_forecast(lat, lng, target_dt)
