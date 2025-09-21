from fastapi import FastAPI
from service.GrafoService import GrafoService
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


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
def calcular_rota():
    return grafo_service.calcular_rota()


