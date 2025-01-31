from datetime import datetime, date
from pydantic import BaseModel, Field

class UsuariosSesionCreate(BaseModel):
    cod_usuario : int
    token_sesion : str = None
    intentos_login : int
    ip_cliente : str

class UsuariosSesionUpdate(UsuariosSesionCreate):
    cod_usuario_sesion : int