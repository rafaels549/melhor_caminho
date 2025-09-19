from fastapi import FastAPI


app = FastAPI()

@app.post("/calcular-rota")
def calcular_rota():
    return {"hello": "world"}
    


