from pydantic import BaseModel, EmailStr
from datetime import datetime, date

class UsuarioCreate(BaseModel):
    identificacion: str
    nombres: str
    apellidos: str
    correo: EmailStr
    tipo_usuario: str
    password: str

class UsuariosLista(BaseModel):
    cod_usuario: int
    identificacion: str
    nombres: str
    apellidos: str
    correo: EmailStr
    created_at: date
    estado_membresia : str
    fecha_vencimiento : date
    cant_comprobantes_permitidos : int

class UsuarioLogin(BaseModel):
    correo: EmailStr
    password: str

class UsuarioRecoverPassword(BaseModel):
    correo: EmailStr
    # token: str = None

class UsuarioValidarToken(BaseModel):
    token: str

class UsuarioUpdatePassword(BaseModel):
    password: str
    confirm_password : str
    correo: EmailStr = None

class UsuarioUpdate(BaseModel):
    identificacion: str
    nombres: str
    apellidos: str
    correo: EmailStr
    

# class Usuarios(BaseModel):
#     cod_usuario: int

#     class Config:
#         from_attributes = True
