import requests
from math import radians, cos, sin, sqrt, atan2
from datetime import datetime
from zoneinfo import ZoneInfo


# --------------------------------------------------
# IPMA endpoints (open data)
# --------------------------------------------------

IPMA_STATIONS_URL = "https://api.ipma.pt/open-data/observation/meteorology/stations.json"
IPMA_OBS_URL = "https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json"


# --------------------------------------------------
# DISTANCE (Haversine)
# --------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# --------------------------------------------------
# METAR TIME FORMAT (DDMMYY HHMM L)
# --------------------------------------------------

def format_metar_time(ts):
    if not ts:
        return "////// ////L"

    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        local = dt.astimezone(ZoneInfo("Europe/Lisbon"))

        date_part = local.strftime("%d%m%y")
        time_part = local.strftime("%H%M") + "L"

        return f"{date_part} {time_part}"

    except:
        return "////// ////L"


# --------------------------------------------------
# METAR-LIKE STRING
# --------------------------------------------------

def format_metar_like(wind_dir, wind_speed, gust, temp, qnh):
    if wind_dir is None or wind_speed is None:
        return "N/A"

    try:
        wind_dir = int(wind_dir)
        wind_speed = int(wind_speed)
    except:
        return "N/A"

    gust_part = f"G{int(gust)}" if gust not in (None, 0) else ""

    temp_part = f"{int(temp)}C" if temp is not None else "N/A"
    qnh_part = f"Q{int(qnh)}" if qnh is not None else "N/A"

    return f"{wind_dir:03d}{wind_speed:02d}{gust_part}KT {temp_part} {qnh_part}"


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def get_ipma_station_weather(lat, lon):

    try:
        stations = requests.get(IPMA_STATIONS_URL, timeout=3).json()
        obs_data = requests.get(IPMA_OBS_URL, timeout=3).json()

        stations_list = stations.get("data", [])
        obs_list = obs_data.get("data", [])

        # --------------------------------------------------
        # 1. find nearest station
        # --------------------------------------------------
        best_station = None
        best_dist = float("inf")

        for s in stations_list:
            try:
                dist = haversine(lat, lon, s.get("lat"), s.get("lon"))

                if dist < best_dist:
                    best_dist = dist
                    best_station = s
            except:
                continue

        if not best_station:
            return None

        station_id = best_station.get("globalIdLocal")

        # --------------------------------------------------
        # 2. find observation
        # --------------------------------------------------
        obs = None
        for o in obs_list:
            if o.get("idEstacao") == station_id:
                obs = o
                break

        if not obs:
            return None

        # --------------------------------------------------
        # 3. build METAR-like string
        # --------------------------------------------------
        metar = format_metar_like(
            obs.get("dirVento"),
            obs.get("intensidadeVento"),
            obs.get("rajadaMax"),
            obs.get("temperatura"),
            obs.get("pressao"),
        )

        # --------------------------------------------------
        # 4. return structured data
        # --------------------------------------------------
        return {
            "metar": metar,
            "distance_km": round(best_dist, 1),
            "station_name": best_station.get("local") or best_station.get("name") or "IPMA Station",
            "obs_time": obs.get("dataHora") or obs.get("timestamp") or obs.get("timeObs")
        }

    except Exception:
        return {
            "metar": "N/A",
            "distance_km": None,
            "station_name": "N/A",
            "obs_time": None
        }