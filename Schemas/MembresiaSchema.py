from pydantic import BaseModel, Field
from datetime import datetime, date

class Membresia(BaseModel):
    nombre_membresia : str = Field(..., max_length=50)
    descripcion_membresia : str
    caracteristicas : str
    precio : float
    cant_comprobantes_carga : int
    estado : str = Field(..., max_length=20)
    fecha_lanzamiento : datetime
    vigencia_meses : int
    fecha_finalizacion : date = None

class MembresiaResponse(Membresia):
    cod_membresia: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
        # orm_mode = True

class lista_memb_disponibles(Membresia):
    cod_membresia: int


class MembresiaUpdate(Membresia):
    cod_membresia : int

class MembresiaVisualizar:
    cod_membresia: int

class PagoMembresia(BaseModel):
    cod_usuario : int = None
    cod_membresia : int
    precio : float
    orderID : str
    estado_membresia : str = None
