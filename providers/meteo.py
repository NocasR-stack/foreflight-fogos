import math
import requests
from datetime import datetime
from zoneinfo import ZoneInfo


# ----------------------------
# COORD DMS
# ----------------------------
def to_dms(value, is_lat=True):
    direction = "N" if value >= 0 else "S" if is_lat else "E" if value >= 0 else "W"

    value = abs(value)
    degrees = int(value)
    minutes_full = (value - degrees) * 60
    minutes = int(minutes_full)
    seconds = round((minutes_full - minutes) * 60, 2)

    return f"{degrees}°{minutes}'{seconds}\"{direction}"


# ----------------------------
# DISTÂNCIA
# ----------------------------
def distance(lat1, lon1, lat2, lon2):
    R = 6371

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ----------------------------
# AIRPORTS (fallback METAR)
# ----------------------------
AIRPORTS = [
    {"name": "Lisboa", "lat": 38.7742, "lon": -9.1342, "icao": "LPPT"},
    {"name": "Porto", "lat": 41.2355, "lon": -8.678, "icao": "LPPR"},
    {"name": "Faro", "lat": 37.0144, "lon": -7.9659, "icao": "LPFR"},
    {"name": "Braga", "lat": 41.5871, "lon": -8.4451, "icao": "LPBR"},
]


def nearest_station(lat, lon):
    closest = None
    min_d = float("inf")

    for a in AIRPORTS:
        d = distance(lat, lon, a["lat"], a["lon"])
        if d < min_d:
            min_d = d
            closest = a

    return closest


# ----------------------------
# METAR FETCH (aero fallback)
# ----------------------------
def get_metar(icao):
    try:
        url = f"https://api.checkwx.com/metar/{icao}/decoded"
        headers = {"X-API-Key": "demo"}

        r = requests.get(url, headers=headers, timeout=5)
        data = r.json()

        if "data" not in data:
            return None

        m = data["data"][0]

        return {
            "wind_dir": m.get("wind", {}).get("degrees"),
            "wind_speed": m.get("wind", {}).get("speed_kts"),
            "temp": m.get("temperature", {}).get("celsius"),
            "qnh": m.get("barometer", {}).get("hpa")
        }

    except:
        return None


# ----------------------------
# IPMA METEO (NOVA CAMADA)
# ----------------------------
def get_ipma_weather(lat, lon):
    try:
        stations_url = "https://api.ipma.pt/open-data/observation/meteorology/stations.json"
        obs_url = "https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json"

        stations = requests.get(stations_url, timeout=3).json().get("data", [])
        obs = requests.get(obs_url, timeout=3).json().get("data", [])

        best = None
        best_d = float("inf")

        for s in stations:
            d = distance(lat, lon, s.get("lat"), s.get("lon"))
            if d < best_d:
                best_d = d
                best = s

        if not best:
            return None

        station_id = best.get("globalIdLocal")

        obs_match = None
        for o in obs:
            if o.get("idEstacao") == station_id:
                obs_match = o
                break

        if not obs_match:
            return None

        wind_dir = obs_match.get("dirVento")
        wind_speed = obs_match.get("intensidadeVento")
        gust = obs_match.get("rajadaMax")
        temp = obs_match.get("temperatura")
        qnh = obs_match.get("pressao")

        # METAR-like
        gust_part = f"G{int(gust)}" if gust else ""
        metar = f"{int(wind_dir):03d}{int(wind_speed):02d}{gust_part}KT {int(temp)}°C Q{int(qnh)}"

        # time
        ts = obs_match.get("dataHora")
        if ts:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            local = dt.astimezone(ZoneInfo("Europe/Lisbon"))
            time_str = local.strftime("%d%m%y %H%M") + "L"
        else:
            time_str = "////// ////L"

        return {
            "metar": metar,
            "station": best.get("local") or best.get("name"),
            "distance": round(best_d, 1),
            "time": time_str
        }

    except:
        return None


# ----------------------------
# ENRICH OCCURRENCE (FINAL)
# ----------------------------
def enrich_occurrence(o):

    lat = o.get("lat")
    lon = o.get("lon")

    # DMS
    o["lat_dms"] = to_dms(lat, True)
    o["lon_dms"] = to_dms(lon, False)

    # ----------------------------
    # IPMA (PRIORIDADE)
    # ----------------------------
    ipma = get_ipma_weather(lat, lon)

    if ipma:
        o["ipma_metar"] = ipma["metar"]
        o["ipma_station"] = ipma["station"]
        o["ipma_distance"] = ipma["distance"]
        o["ipma_time"] = ipma["time"]

    # ----------------------------
    # FALLBACK METAR AEROPORTO
    # ----------------------------
    station = nearest_station(lat, lon)

    if station:
        meteo = get_metar(station["icao"])

        o["meteo_station"] = station["name"]

        if meteo:
            o["wind_dir"] = meteo.get("wind_dir")
            o["wind_speed"] = meteo.get("wind_speed")
            o["temp"] = meteo.get("temp")
            o["qnh"] = meteo.get("qnh")

    return o