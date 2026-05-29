
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse

from providers.ptdata import get_occurrences
from generator.kml import build_kml

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok", "message": "ForeFlight Fogos API running"}


@app.get("/fogos.kml")
def fogos_kml():
    occurrences = get_occurrences()
    kml = build_kml(occurrences)

    return Response(content=kml, media_type="application/vnd.google-earth.kml+xml")


# 🔥 DEBUG endpoint (para análise dos dados)
@app.get("/debug/occurrences")
def debug_occurrences():
    data = get_occurrences()
    return JSONResponse(content=data)
