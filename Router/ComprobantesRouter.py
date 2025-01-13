from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from Logica.ComprobantesLogica import ComprobantesLogica

from Schemas.ComprobantesSchema import ParametrosExtraccion
from Schemas.ComprobantesSchema import CompradorResponse
from Schemas.ComprobantesSchema import CombantesResponse
from Schemas.ComprobantesSchema import ComprobantesLista
from Schemas.ComprobantesSchema import DetallesResponse
from Schemas.ComprobantesSchema import DetallesUpdate


from Persistencia.Conexion import DataBase

router = APIRouter()
ComprobantesLogica = ComprobantesLogica()
# comprobantes
@router.post('/extraer_comprobantes')
def extraer_comprobantes(datos : ParametrosExtraccion):
    return ComprobantesLogica.extraer_comprobantes(datos)

@router.post('/cargar_comprobantes')
def cargar_comprobantes( db : Session = Depends(DataBase.get_db)):
    return ComprobantesLogica.cargar_comprobantes(db)

@router.post('/lista_comprobantes', response_model=List[CombantesResponse])
def lista_comprobantes( datos : ComprobantesLista, db : Session = Depends(DataBase.get_db)):
    return ComprobantesLogica.lista_comprobantes(datos, db)

# compradores
@router.post('/lista_compradores', response_model=List[CompradorResponse])
def lista_compradores( db : Session = Depends(DataBase.get_db)):
    return ComprobantesLogica.lista_compradores(db)

# detalles
@router.get('/detalles_comprobante/{cod_comprobante}', response_model=List[DetallesResponse])
def detalles_comprobante( cod_comprobante : int, db : Session = Depends(DataBase.get_db)):
    return ComprobantesLogica.detalles_comprobante(cod_comprobante, db)

@router.post('/detalles_update')
def detalles_update( datos : DetallesUpdate, db : Session = Depends(DataBase.get_db)):
    return ComprobantesLogica.detalles_update(datos, db)