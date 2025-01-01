from pydantic import BaseModel
from datetime import date

class UsuarioMembresiaCreate(BaseModel):
    cod_usuario: str
    cod_membresia: str
    order_id_paypal : str
    estado_membresia : str

class UsuarioMembresia(BaseModel):
    cod_usuario : str
    cod_membresia : str
    nombre_membresia : str
    descripcion_membresia : str
    caracteristicas : str
    estado_membresia : str
    fecha_vencimiento: date
    fecha_compra : date
    order_id_paypal : str