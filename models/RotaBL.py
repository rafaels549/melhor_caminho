from pydantic import BaseModel
from typing import Optional

class RotaBL(BaseModel):
    initial_solution: int
    methodSelect: str
    TP: Optional[int] = None
    NG: Optional[int] = None
    TC: Optional[float] = None
    TM: Optional[float] = None
    IG: Optional[float] = None
    limite: Optional[int] = None
    initial_temp: Optional[float] = None
    final_temp: Optional[float] = None
    cooling_rate: Optional[float] = None

#---------------------------------------------------------------------