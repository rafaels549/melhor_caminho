from fastapi import FastAPI
from service.GrafoService import GrafoService
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.Rota import Rota


app = FastAPI()
app.mount("/static", StaticFiles(directory="views"), name="static")
grafo_service = GrafoService()


@app.get("/")
def read_root():
    return FileResponse("views/index.html")

@app.get("/gera_grafo")
def gera_grafo():

    return grafo_service.gera_grafo()

@app.post("/calcular-rota")
def calcular_rota(rota: Rota):
    start = rota.start
    end = rota.end
    method = rota.method
    return grafo_service.calcular_rota(start, end, method)

