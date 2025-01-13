from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    identificacion: str
    nombres: str
    apellidos: str
    correo: EmailStr
    tipo_usuario: str
    password: str

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

# class Usuarios(BaseModel):
#     cod_usuario: int

#     class Config:
#         from_attributes = True
