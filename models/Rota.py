from pydantic import BaseModel
from typing import Optional

class Rota(BaseModel):
    start: str
    end: str
    method: str
    limite: Optional[int] = None 