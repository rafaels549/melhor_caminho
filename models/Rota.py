from pydantic import BaseModel

class Rota(BaseModel):
    start: str
    end: str
    method: str