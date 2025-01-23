from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from Logica.AgpLogica import AgpLogica
from Schemas.AnexoGatosPersonalesSchema import AgpDatosConsulta, AgpDatos, AgpDatosGenerarXml   

from Persistencia.Conexion import DataBase

router = APIRouter()
AgpLogica = AgpLogica()

@router.get('/agp_datos_lista/{identificacion_comprador}/{cod_periodo_fiscal}', response_model=List[AgpDatos])
def agp_datos_lista( identificacion_comprador : str, cod_periodo_fiscal : int , db : Session = Depends(DataBase.get_db)):
    return AgpLogica.agp_datos_lista(identificacion_comprador, cod_periodo_fiscal, db)

@router.post('/generar_agp', response_model=List[AgpDatos])
def generar_agp(datos : AgpDatosGenerarXml, db : Session = Depends(DataBase.get_db)):
    return AgpLogica.generar_agp(datos, db)

# @router.get('/categorias_lista' , response_model=List[CategoriaLista])
# def categorias_lista(db : Session = Depends(DataBase.get_db)):
#     return CategoriasLogica.categorias_lista(db)