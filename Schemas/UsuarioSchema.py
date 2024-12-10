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

class Usuarios(BaseModel):
    cod_usuario: str

    class Config:
        from_attributes = True
