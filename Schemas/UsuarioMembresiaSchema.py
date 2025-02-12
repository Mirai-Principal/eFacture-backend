from pydantic import BaseModel
from datetime import date

class UsuarioMembresiaCreate(BaseModel):
    cod_usuario: int
    cod_membresia: int
    order_id_paypal : str
    estado_membresia : str
    cant_comprobantes_permitidos : int

class UsuarioMembresia(BaseModel):
    cod_usuario : int
    cod_membresia : int
    nombre_membresia : str
    descripcion_membresia : str
    caracteristicas : str
    estado_membresia : str
    fecha_vencimiento: date
    cant_comprobantes_permitidos : int
    fecha_compra : date
    order_id_paypal : str
    cant_comprobantes_carga : int

class MiSuscripcion(BaseModel):
    cod_usuario : int
    cod_membresia : int

class EstadoSuscripcion(BaseModel):
    estado_membresia : str