from fastapi import APIRouter, Depends, HTTPException, Request
import json
from sqlalchemy.orm import Session
from typing import List

from Logica.MembresiasLogica import MembresiasLogica
from Logica import Auth
from Schemas import MembresiaSchema

from Persistencia.Conexion import DataBase

router = APIRouter()
MembresiasLogica = MembresiasLogica()

@router.get("/lista_membresias", response_model=List[MembresiaSchema.MembresiaResponse])
def lista_membresias( db: Session = Depends(DataBase.get_db)):
    return MembresiasLogica.lista_membresias( db)

@router.post("/nueva_membresia")
def nueva_membresia(datos:MembresiaSchema.Membresia , db: Session = Depends(DataBase.get_db)):
    return MembresiasLogica.nueva_membresia(datos, db)

@router.post("/actualizar_membresia")
def actualizar_membresia(datos : MembresiaSchema.MembresiaUpdate, db : Session = Depends(DataBase.get_db)):
    return MembresiasLogica.actualizar_membresia(datos, db)

@router.get('/visualizar_membresia/{cod_membresia}', response_model = None)
def visualizar_membresia(cod_membresia : str, db : Session = Depends(DataBase.get_db)):
    return MembresiasLogica.visualizar_membresia(cod_membresia, db)







