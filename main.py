from fastapi import FastAPI
from models.GerarGrafoBL import GerarGrafoBL
from models.RotaBL import RotaBL
from service.GrafoService import GrafoService
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.Rota import Rota
from typing import Optional
from ag_pcv import (AlgoritmoGenetico, GerarProblema)


app = FastAPI()
app.mount("/static", StaticFiles(directory="views"), name="static")
grafo_service = GrafoService()


@app.get("/")
def read_root():
    return FileResponse("views/index.html")

@app.get("/busca_local_metaheuristicas")
def busca_local_metaheuristicas():
    return FileResponse("views/busca_local_metaheuristicas.html")

@app.post("/calcular-rota-bl")
def calcular_rota_bl(rota: RotaBL):
    mat = GerarProblema(rota.initial_solution, 1, 100)
    grafo_service._matriz = mat
    resultado = grafo_service.calcular_algoritmo_genetico(
        metodo=rota.methodSelect,
        mat=grafo_service._matriz,
        tp=rota.TP,
        ng=rota.NG,
        tc=rota.TC,
        tm=rota.TM,
        ig=rota.IG,
        limite=rota.limite,
        t_ini=rota.initial_temp,
        t_fim=rota.final_temp,
        fr=rota.cooling_rate
        
    )
    return  resultado

@app.post("/gera_grafo_bl")
def gera_grafo_bl(gerar_grafo: GerarGrafoBL):
    quantidade_nos = gerar_grafo.numeroDeNos
    min_value = gerar_grafo.minValue
    max_value = gerar_grafo.maxValue
    mat = GerarProblema(quantidade_nos, min_value, max_value)
    base64 = grafo_service.gerar_grafo_bl(mat)
    return {"imagem_base64": base64 , "matriz": mat.tolist()}

@app.get("/gera_grafo")
def gera_grafo(name: Optional[str] = None):
    grafo_service = GrafoService(name)
    return grafo_service.gera_grafo()

@app.post("/calcular-rota")
def calcular_rota(rota: Rota):
    start = rota.start
    end = rota.end
    method = rota.method
    limite = rota.limite
    tipoGrafo = rota.tipoGrafo
    if limite is not None:
       return grafo_service.calcular_rota(start, end, method, tipoGrafo, limite)
    else:
        return grafo_service.calcular_rota(start, end, method,tipoGrafo)

@app.get("/gerar_relatorio")
def gerar_relatorio():
    return grafo_service.gerar_relatorio()