
import requests


def get_weather(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "wind_speed_10m",
            "wind_direction_10m",
            "pressure_msl"
        ],
        "windspeed_unit": "kn",
        "timezone": "auto"
    }

    try:
        r = requests.get(url, params=params, timeout=2)
        data = r.json()

        current = data.get("current", {})

        return {
            "temp": current.get("temperature_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "wind_dir": current.get("wind_direction_10m"),
            "qnh": current.get("pressure_msl")
        }

    except:
        return {
            "temp": "N/A",
            "wind_speed": "N/A",
            "wind_dir": "N/A",
            "qnh": "N/A"
        }
