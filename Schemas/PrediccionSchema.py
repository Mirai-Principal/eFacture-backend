from datetime import datetime, date
from pydantic import BaseModel, Field


class DatasetEntrenamientoCreate(BaseModel):
    usuario : str
    fecha : date
    categoria : str
    monto : float