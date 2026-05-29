from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
import time

from providers.ptdata import get_occurrences
from generator.kml import build_kml

app = FastAPI()

# ----------------------------
# CACHE (melhora performance)
# ----------------------------
_cache_geojson = None
_cache_kml = None
_cache_time = 0
CACHE_SECONDS = 30


# ----------------------------
# KML ENDPOINT (ForeFlight)
# ----------------------------
@app.get("/fogos.kml")
def fogos_kml():
    global _cache_kml, _cache_time

    now = time.time()

    if _cache_kml and (now - _cache_time) < CACHE_SECONDS:
        return Response(content=_cache_kml, media_type="application/vnd.google-earth.kml+xml")

    data = get_occurrences()
    kml = build_kml(data)

    _cache_kml = kml
    _cache_time = now

    return Response(content=kml, media_type="application/vnd.google-earth.kml+xml")


# ----------------------------
# GEOJSON ENDPOINT (novo motor)
# ----------------------------
@app.get("/fogos.geojson")
def fogos_geojson():
    global _cache_geojson, _cache_time

    now = time.time()

    if _cache_geojson and (now - _cache_time) < CACHE_SECONDS:
        return JSONResponse(_cache_geojson)

    data = get_occurrences()

    features = []

    for o in data:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [o.get("lon"), o.get("lat")]
            },
            "properties": {
                "id": o.get("id"),
                "parish": o.get("parish"),
                "district": o.get("district"),
                "municipality": o.get("municipality"),
                "nature": o.get("nature_desc"),
                "status": o.get("status"),
                "status_code": o.get("status_code"),
                "aerial": o.get("aerial"),
                "ground": o.get("ground"),
                "operatives": o.get("operatives"),
                "started_at": o.get("started_at")
            }
        })

    result = {
        "type": "FeatureCollection",
        "features": features
    }

    _cache_geojson = result
    _cache_time = now

    return JSONResponse(result)


# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "foreflight-fogos",
        "endpoints": [
            "/fogos.kml",
            "/fogos.geojson"
        ]
    }