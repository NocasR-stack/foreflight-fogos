from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
import time

from providers.ptdata import get_occurrences
from providers.meteo import enrich_occurrence
from generator.kml import build_kml

app = FastAPI()

_cache_geojson = None
_cache_kml = None
_cache_time = 0
CACHE_SECONDS = 30


# ----------------------------
# KML
# ----------------------------
@app.get("/fogos.kml")
def fogos_kml():
    global _cache_kml, _cache_time

    now = time.time()

    if _cache_kml and (now - _cache_time) < CACHE_SECONDS:
        return Response(
            content=_cache_kml,
            media_type="application/vnd.google-earth.kml+xml",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )

    data = get_occurrences()

    enriched = [enrich_occurrence(o) for o in data]

    kml = build_kml(enriched)

    _cache_kml = kml
    _cache_time = now

    return Response(
        content=kml,
        media_type="application/vnd.google-earth.kml+xml",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


# ----------------------------
# GEOJSON
# ----------------------------
@app.get("/fogos.geojson")
def fogos_geojson():
    global _cache_geojson, _cache_time

    now = time.time()

    if _cache_geojson and (now - _cache_time) < CACHE_SECONDS:
        return JSONResponse(_cache_geojson)

    data = get_occurrences()

    enriched = [enrich_occurrence(o) for o in data]

    features = []

    for o in enriched:
        try:
            lat = float(o.get("lat"))
            lon = float(o.get("lon"))

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "id": o.get("id"),
                    "parish": o.get("parish"),
                    "status_code": o.get("status_code"),
                    "aerial": o.get("aerial"),
                    "ground": o.get("ground"),
                    "operatives": o.get("operatives"),
                    "lat_dms": o.get("lat_dms"),
                    "lon_dms": o.get("lon_dms"),
                    "wind_dir": o.get("wind_dir"),
                    "wind_speed": o.get("wind_speed"),
                    "temp": o.get("temp"),
                    "qnh": o.get("qnh"),
                    "meteo_station": o.get("meteo_station")
                }
            })

        except Exception:
            continue

    result = {
        "type": "FeatureCollection",
        "features": features
    }

    _cache_geojson = result
    _cache_time = now

    return JSONResponse(result)


# ----------------------------
# ROOT
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "endpoints": [
            "/fogos.kml",
            "/fogos.geojson"
        ]
    }