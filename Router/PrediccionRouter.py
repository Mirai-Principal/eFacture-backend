from fastapi import APIRouter, Depends, Request
from typing import List
from sqlalchemy.orm import Session

from Logica.PrediccionLogica import PrediccionLogica
from Schemas.PrediccionSchema import DatosPrediccion, DatosHistorico, DatosCategoricos, CategoricoMensual

from Persistencia.Conexion import DataBase

router = APIRouter()
PrediccionLogica = PrediccionLogica()


# @router.get('/agp_datos_lista/{identificacion_comprador}/{cod_periodo_fiscal}', response_model=List[AgpDatos])
# def agp_datos_lista( identificacion_comprador : str, cod_periodo_fiscal : int , db : Session = Depends(DataBase.get_db)):
#     return AgpLogica.agp_datos_lista(identificacion_comprador, cod_periodo_fiscal, db)

@router.get('/generar_dataset')
def generar_dataset(db : Session = Depends(DataBase.get_db)):
    return PrediccionLogica.generar_dataset( db)

@router.get('/consultar_prediccion/{usuario}/{categoria}', response_model = List[DatosPrediccion])
def consultar_prediccion(usuario : str, categoria : str, db : Session = Depends(DataBase.get_db)):
    return PrediccionLogica.consultar_prediccion(usuario, categoria, db)

@router.get('/consultar_historico/{usuario}/{categoria}', response_model = List[DatosHistorico])
def consultar_historico(usuario : str, categoria : str,db : Session = Depends(DataBase.get_db)):
    return PrediccionLogica.consultar_historico(usuario, categoria, db)

@router.get('/consultar_prediccion_categorico/{usuario}', response_model = List[DatosCategoricos])
def consultar_prediccion_categorico(usuario : str, db : Session = Depends(DataBase.get_db)):
    return PrediccionLogica.consultar_prediccion_categorico(usuario, db)

@router.get('/consultar_historico_categorico/{usuario}', response_model = List[DatosCategoricos])
def consultar_historico_categorico(usuario : str, db : Session = Depends(DataBase.get_db)):
    return PrediccionLogica.consultar_historico_categorico(usuario, db)

# cara obtener datos en range de prediccion del frontend
@router.get('/consultar_categorico_mensual/{categoria}/{mes}/{usuario}', response_model = List[CategoricoMensual])
def consultar_categorico_mensual(categoria: str, mes : int, usuario : str, db : Session = Depends(DataBase.get_db)):
    return PrediccionLogica.consultar_categorico_mensual(categoria, mes, usuario, db)
