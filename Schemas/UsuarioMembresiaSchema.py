from pydantic import BaseModel
from datetime import date

class UsuarioMembresiaCreate(BaseModel):
    cod_usuario: int
    cod_membresia: int
    order_id_paypal : str
    estado_membresia : str

class UsuarioMembresia(BaseModel):
    cod_usuario : int
    cod_membresia : int
    nombre_membresia : str
    descripcion_membresia : str
    caracteristicas : str
    estado_membresia : str
    fecha_vencimiento: date
    fecha_compra : date
    order_id_paypal : str