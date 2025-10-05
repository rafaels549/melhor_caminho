from pydantic import BaseModel
from typing import Optional

class Rota(BaseModel):
    start: str
    end: str
    method: str
    limite: Optional[int] = None 
    tipoGrafo: str = "grafo_sem_pesos"