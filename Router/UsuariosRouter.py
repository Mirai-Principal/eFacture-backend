from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from Logica import Dependencies, Auth
from Schemas import UsuarioSchema
from CRUD import UsuariosCrud



router = APIRouter()

@router.get("/")
def probando():
    return {"message": "Lista de usuarios"}

@router.post("/registrar", response_model=UsuarioSchema.UsuarioCreate)
def registrar(user: UsuarioSchema.UsuarioCreate, db: Session = Depends(Dependencies.get_db)):
    print(user.dict())
    correo_existe = UsuariosCrud.get_user_by_email(db, user.correo)
    if correo_existe:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    identificacion_existe = UsuariosCrud.get_user_by_identificacion(db, user.identificacion)
    if identificacion_existe:
        raise HTTPException(status_code=400, detail="Identificación ya registrada")
    return UsuariosCrud.create_user(db=db, user=user)


@router.post("/login")
def login(user: UsuarioSchema.UsuarioLogin, db: Session = Depends(Dependencies.get_db)):
    db_user = UsuariosCrud.get_user_by_email(db, user.correo)
    if db_user is None or not UsuariosCrud.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    access_token = Auth.create_access_token(data={"sub": db_user.correo})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/validate_token")
def validate_token(user: dict = Depends(Auth.verify_token), db: Session = Depends(Dependencies.get_db)):
    # Aquí podrías devolver datos específicos del usuario autenticado
    return {"message": f"Bienvenido al panel, usuario {user['sub']}"}