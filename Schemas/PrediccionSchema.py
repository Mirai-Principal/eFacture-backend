from datetime import datetime, date
from pydantic import BaseModel, Field


class DatasetEntrenamientoCreate(BaseModel):
    usuario : str
    fecha : date
    categoria : str
    monto : float

class DatosPrediccion(DatasetEntrenamientoCreate):
    mes : int
    anio : int

class DatosHistorico(BaseModel):
    anio_mes : date
    monto : float

class DatosCategoricos(BaseModel):
    categoria : str
    monto : float

class CategoricoMensual(BaseModel):
    anio : int
    monto : float
    