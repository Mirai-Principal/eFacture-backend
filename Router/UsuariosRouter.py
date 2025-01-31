from fastapi import APIRouter, Depends, Request, Response
from typing import List


from fastapi.security import OAuth2PasswordBearer
# import json
from sqlalchemy.orm import Session

from Logica.UsuariosLogica import UsuariosLogica
from Schemas.UsuarioSchema import (UsuarioCreate, UsuarioLogin, UsuarioRecoverPassword,
                                    UsuarioUpdatePassword, UsuarioUpdate, UsuariosLista, )

from Persistencia.Conexion import DataBase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="cambiar_password")

router = APIRouter()

UsuariosLogica = UsuariosLogica()

@router.get("/")
def index():
    return {"message": "eFacture API"}

@router.post("/registrar", response_model=UsuarioCreate)
def registrar_usuario(user: UsuarioCreate, db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.registrar_usuario(user, db)

@router.post("/login")
def login(request: Request, user: UsuarioLogin, db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.login(request, user, db)

@router.post("/password_reset")
def password_reset(request: Request, data: UsuarioRecoverPassword,  db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.password_reset(request, data, db)

@router.post("/cambiar_password")
def cambiar_password(data: UsuarioUpdatePassword, db: Session = Depends(DataBase.get_db), token: str = Depends(oauth2_scheme)):
    return UsuariosLogica.cambiar_password(token, data, db)

@router.post("/validate_token")
def validate_token(request : Request):
    return {"message": "Token válido"}

@router.get("/clientes_lista", response_model=List[UsuariosLista])
def usuarios_lista(db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.clientes_lista(db)

@router.get("/usuario")
def usuario_by_correo(request : Request, db = Depends(DataBase.get_db)):
    return UsuariosLogica.usuario_by_correo(request, db)

# actualizar usuario
@router.post("/usuario")
def usuario_update(datos : UsuarioUpdate, db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.usuario_update(datos, db)  