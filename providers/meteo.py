import math
import requests


# ----------------------------
# CONVERTER COORDENADAS PARA DMS
# ----------------------------
def to_dms(value, is_lat=True):
    direction = ""
    if is_lat:
        direction = "N" if value >= 0 else "S"
    else:
        direction = "E" if value >= 0 else "W"

    value = abs(value)
    degrees = int(value)
    minutes_full = (value - degrees) * 60
    minutes = int(minutes_full)
    seconds = round((minutes_full - minutes) * 60, 2)

    return f"{degrees}°{minutes}'{seconds}\"{direction}"


# ----------------------------
# DISTÂNCIA SIMPLES (Haversine)
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
# ESTAÇÃO METEO MAIS PRÓXIMA (METAR simples via aeroportos)
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
# METAR FETCH (AVWX API opcional)
# ----------------------------
def get_metar(icao):
    try:
        url = f"https://api.checkwx.com/metar/{icao}/decoded"
        headers = {"X-API-Key": "demo"}  # pode ser substituído por API key real

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
# ENRICH OCCURRENCE
# ----------------------------
def enrich_occurrence(o):
    lat = o.get("lat")
    lon = o.get("lon")

    # DMS
    o["lat_dms"] = to_dms(lat, True)
    o["lon_dms"] = to_dms(lon, False)

    # METEO
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