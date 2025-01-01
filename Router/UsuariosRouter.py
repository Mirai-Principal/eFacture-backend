from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordBearer
# import json
from sqlalchemy.orm import Session

from Logica.UsuariosLogica import UsuariosLogica
from Schemas import UsuarioSchema


from Persistencia.Conexion import DataBase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="cambiar_password")

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

@router.post("/password_reset")
def password_reset(request: Request, data: UsuarioSchema.UsuarioRecoverPassword,  db: Session = Depends(DataBase.get_db)):
    return UsuariosLogica.password_reset(request, data, db)

@router.post("/cambiar_password")
def cambiar_password(data: UsuarioSchema.UsuarioUpdatePassword, db: Session = Depends(DataBase.get_db), token: str = Depends(oauth2_scheme)):
    return UsuariosLogica.cambiar_password(token, data, db)

@router.post("/validate_token")
def validate_token(request : Request):
    return {"message": "Token válido"}
