from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from Logica.SueldoBasicoLogica import SueldoBasicoLogica
from Schemas.SueldoBasicoSchema import SueldoBasicoCreate, SueldoBasicoLista

from Persistencia.Conexion import DataBase

router = APIRouter()

SueldoBasicoLogica = SueldoBasicoLogica()

@router.post('/sueldo_basico_insert')
def sueldo_basico_insert( datos : SueldoBasicoCreate, db : Session = Depends(DataBase.get_db)):
    return SueldoBasicoLogica.sueldo_basico_insert(datos, db)

@router.get('/lista_sueldo_basico' , response_model=List[SueldoBasicoLista])
def lista_sueldo_basico(db : Session = Depends(DataBase.get_db)):
    return SueldoBasicoLogica.lista_sueldo_basico(db)