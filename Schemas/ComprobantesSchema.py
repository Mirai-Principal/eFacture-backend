from datetime import datetime, date
from pydantic import BaseModel, Field

#? paramtros extraccion
class ParametrosExtraccion(BaseModel):
    identificacion : str = Field(..., max_length=13)
    password : str
    anio : str
    mes : str
    dia : str

#? Comprador
class CompradorCreate(BaseModel):
    identificacion_comprador: str = Field(..., max_length=13)
    razon_social_comprador : str = Field(..., max_length=100)

class CompradorResponse(CompradorCreate):
    cod_comprador : int

#? Comprobantes
class ComprobantesCreate(BaseModel):
    cod_comprador : int
    archivo : str
    clave_acceso : str
    razon_social : str = Field(..., max_length=100)
    fecha_emision : datetime
    importe_total : float

class CombantesResponse(ComprobantesCreate):
    cod_comprobante : int
    cod_comprador : int
    clave_acceso : str
    razon_social : str = Field(..., max_length=100)
    fecha_emision : date
    importe_total : float

class ComprobantesLista(BaseModel):
    cod_comprador : int = None
    identificacion : str = Field(..., max_length=13)
    anio : str
    mes : str
    dia : int | str

#? Detalles
class DetallesCreate(BaseModel):
    cod_categoria : int
    cod_comprobante : int = 1
    descripcion : str
    cantidad : int
    precio_unitario : float
    precio_total_sin_impuesto : float
    impuesto_valor : float
    detalle_valor : float

class DetallesResponse(DetallesCreate):
    cod_detalle : int
    
class DetallesUpdate(BaseModel):
    cod_categoria : int
    cod_detalle : int
