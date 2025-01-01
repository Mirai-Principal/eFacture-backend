from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from typing import List

from Logica.MembresiasLogica import MembresiasLogica
from Schemas import MembresiaSchema

from Persistencia.Conexion import DataBase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="generar_suscripcion")


router = APIRouter()
MembresiasLogica = MembresiasLogica()

@router.get("/lista_membresias", response_model=List[MembresiaSchema.MembresiaResponse])
def lista_membresias( db: Session = Depends(DataBase.get_db)):
    return MembresiasLogica.lista_membresias( db)

@router.get("/lista_memb_disponibles", response_model=List[MembresiaSchema.lista_memb_disponibles])
def lista_memb_disponibles( db: Session = Depends(DataBase.get_db)):
    return MembresiasLogica.lista_memb_disponibles( db)

@router.post("/nueva_membresia")
def nueva_membresia(datos:MembresiaSchema.Membresia , db: Session = Depends(DataBase.get_db)):
    return MembresiasLogica.nueva_membresia(datos, db)

@router.post("/actualizar_membresia")
def actualizar_membresia(datos : MembresiaSchema.MembresiaUpdate, db : Session = Depends(DataBase.get_db)):
    return MembresiasLogica.actualizar_membresia(datos, db)

@router.get('/visualizar_membresia/{cod_membresia}', response_model = None)
def visualizar_membresia(cod_membresia : str, db : Session = Depends(DataBase.get_db)):
    return MembresiasLogica.visualizar_membresia(cod_membresia, db)

@router.post("/generar_suscripcion")
def generar_suscripcion(datos : MembresiaSchema.PagoMembresia , db: Session = Depends(DataBase.get_db), token: str = Depends(oauth2_scheme)):
    return MembresiasLogica.generar_suscripcion(token, datos, db)