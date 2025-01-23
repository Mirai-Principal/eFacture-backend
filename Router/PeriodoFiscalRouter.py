from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from Logica.PeriodoFiscalLogica import PeriodoFiscal
from Schemas.PeriodoFiscalSchema import PeriodoFiscalCreate, PeriodoFiscalLista, PeriodoFiscalDetele

from Persistencia.Conexion import DataBase

router = APIRouter()
PeriodoFiscal = PeriodoFiscal()

@router.post('/periodo_fiscal_insert')
def periodo_fiscal_insert( datos : PeriodoFiscalCreate, db : Session = Depends(DataBase.get_db)):
    return PeriodoFiscal.periodo_fiscal_insert(datos, db)

@router.get('/periodo_fiscal_lista' , response_model=List[PeriodoFiscalLista])
def periodo_fiscal_lista(db : Session = Depends(DataBase.get_db)):
    return PeriodoFiscal.periodo_fiscal_lista(db)

# select en fraccion basica
@router.get('/periodo_fiscal_lista_select' , response_model=List[PeriodoFiscalLista])
def periodo_fiscal_lista_select(db : Session = Depends(DataBase.get_db)):
    return PeriodoFiscal.periodo_fiscal_lista(db)

@router.post('/periodo_fiscal_delete' )
def periodo_fiscal_delete(datos: PeriodoFiscalDetele, db : Session = Depends(DataBase.get_db)):
    return PeriodoFiscal.periodo_fiscal_delete(datos, db)
