from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from Logica.PrediccionLogica import PrediccionLogica
from Schemas.PrediccionSchema import DatasetEntrenamientoCreate

from Persistencia.Conexion import DataBase

router = APIRouter()
PrediccionLogica = PrediccionLogica()


# @router.get('/agp_datos_lista/{identificacion_comprador}/{cod_periodo_fiscal}', response_model=List[AgpDatos])
# def agp_datos_lista( identificacion_comprador : str, cod_periodo_fiscal : int , db : Session = Depends(DataBase.get_db)):
#     return AgpLogica.agp_datos_lista(identificacion_comprador, cod_periodo_fiscal, db)

@router.get('/generar_dataset')
def generar_dataset(db : Session = Depends(DataBase.get_db)):
    return PrediccionLogica.generar_dataset( db)

@router.get('/consultar_prediccion/{usuario}/{categoria}')
def consultar_prediccion(usuario, categoria, db : Session = Depends(DataBase.get_db)):
    return PrediccionLogica.consultar_prediccion(usuario, categoria, db)