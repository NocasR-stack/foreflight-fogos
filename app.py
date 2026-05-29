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
# ROOT (HEALTH CHECK + HEAD FIX)
# ----------------------------
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {
        "status": "ok",
        "service": "fogos-api",
        "endpoints": [
            "/fogos.kml",
            "/fogos.geojson"
        ]
    }


# ----------------------------
# KML (FOREFLIGHT OPTIMIZED)
# ----------------------------
@app.get("/fogos.kml")
def fogos_kml():
    global _cache_kml, _cache_time

    now = time.time()
    cache_buster = str(int(now))

    if _cache_kml and (now - _cache_time) < CACHE_SECONDS:
        return Response(
            content=_cache_kml,
            media_type="application/vnd.google-earth.kml+xml",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
                "X-Cache-Buster": cache_buster
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
            "Expires": "0",
            "X-Cache-Buster": cache_buster
        }
    )


# ----------------------------
# GEOJSON (DEBUG PASSO 1)
# ----------------------------
@app.get("/fogos.geojson")
def fogos_geojson():

    data = get_occurrences()

    return {
        "count": len(data),
        "first_item": data[0] if data else None
    }