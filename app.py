from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
import time

from providers.ptdata import get_occurrences
from providers.meteo import enrich_occurrence
from generator.kml import build_kml

app = FastAPI()

_cache_kml = None
_cache_time = 0
CACHE_SECONDS = 30


@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {
        "status": "ok",
        "service": "fogos-api",
        "endpoints": [
            "/fogos.kml"
        ]
    }


@app.get("/fogos.kml")
def fogos_kml():

    data = get_occurrences()
    enriched = [enrich_occurrence(o) for o in data]

    kml = build_kml(enriched)

    now = str(int(time.time()))

    return Response(
        content=kml,
        media_type="application/vnd.google-earth.kml+xml",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
            "ETag": now
        }
    )


@app.get("/fogos.geojson")
def fogos_geojson():
    data = get_occurrences()

    return {
        "count": len(data),
        "items": data
    }