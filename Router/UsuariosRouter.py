from fastapi import APIRouter, Depends, HTTPException, Request
import json
from sqlalchemy.orm import Session

from Logica.UsuariosLogica import UsuariosLogica
from Logica import Auth
from Persistencia.Schemas import UsuarioSchema

from Persistencia.Conexion import DataBase

router = APIRouter()

UsuariosLogica = UsuariosLogica()

@router.get("/")
def index():
    return {"message": "eFacture API"}

@router.post("/registrar", response_model=UsuarioSchema.UsuarioCreate)
def registrar_usuario(user: UsuarioSchema.UsuarioCreate, db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.registrar_usuario(user, db)


@router.post("/login")
def login(user: UsuarioSchema.UsuarioLogin, db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.login(user, db)

@router.post("/validate_token")
def validate_token(data: UsuarioSchema.UsuarioValidarToken):
    # Aquí podrías devolver datos específicos del usuario autenticado
    return Auth.verify_token(data.token)

@router.post("/password_reset")
def password_reset(request: Request, data: UsuarioSchema.UsuarioRecoverPassword,  db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.password_reset(request, data, db)

@router.post("/cambiar_password")
def cambiar_password(data: UsuarioSchema.UsuarioUpdatePassword, db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.cambiar_password(data, db)









