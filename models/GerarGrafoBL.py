from pydantic import BaseModel
from typing import Optional

class GerarGrafoBL(BaseModel):
    numeroDeNos: Optional[int] = 30
    minValue: int 
    maxValue: int