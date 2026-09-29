"""Satellite cross-check."""
from __future__ import annotations
from datetime import datetime

import httpx

from backend.config import settings
from backend.utils.logger import logger


class SatelliteCrossCheck:
    OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.log = logger.bind(service="satellite_crosscheck")
        self._client = httpx.Client(timeout=10.0)

    def check_consistency(self, latitude, longitude, claimed_date):
        weather = self._fetch_weather(latitude, longitude)
        if not weather:
            return {"score": 0.5, "available": False, "reason": "Satellite cross-check unavailable"}
        score, reason = self._score_weather(weather, claimed_date)
        return {
            "score": score,
            "available": True,
            "reason": reason,
            "weather": {
                "condition": weather.get("weather", [{}])[0].get("main", "Unknown"),
                "temp_c": round(weather.get("main", {}).get("temp", 0) - 273.15, 1),
                "humidity": weather.get("main", {}).get("humidity"),
            },
        }

    def close(self):
        self._client.close()

    def _fetch_weather(self, lat, lon):
        if not settings.openweather_api_key:
            return None
        try:
            r = self._client.get(
                self.OPENWEATHER_URL,
                params={"lat": lat, "lon": lon, "appid": settings.openweather_api_key},
            )
            r.raise_for_status()
            return r.json()
        except Exception as e:
            self.log.warning("Weather fetch failed: " + str(e))
            return None

    def _score_weather(self, weather, claimed_date):
        main = weather.get("weather", [{}])[0].get("main", "").lower()
        if main in ("rain", "thunderstorm", "drizzle"):
            return 0.9, "Weather consistent: " + main
        if main == "clouds":
            return 0.7, "Weather partially consistent (cloudy)"
        if main == "clear":
            return 0.5, "Clear weather - verify visual evidence manually"
        return 0.6, "Weather condition: " + main
