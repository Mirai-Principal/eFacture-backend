from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from Logica.CategoriasLogica import CategoriasLogica
from Schemas.CategoriasSchema import CategoriaCreate, CategoriaLista, CategoriasUnicas

from Persistencia.Conexion import DataBase

router = APIRouter()
CategoriasLogica = CategoriasLogica()

@router.post('/categorias_insert')
def categorias_insert( datos : CategoriaCreate, db : Session = Depends(DataBase.get_db)):
    if datos.cod_categoria != 0:
        return CategoriasLogica.categoria_update(datos, db)
    return CategoriasLogica.categoria_insert(datos, db)

@router.get('/categorias_lista' , response_model=List[CategoriaLista])
def categorias_lista(db : Session = Depends(DataBase.get_db)):
    return CategoriasLogica.categorias_lista(db)

@router.get('/categorias_por_periodo_lista/{cod_fraccion_basica}' , response_model=List[CategoriaLista])
def categorias_por_periodo_lista(cod_fraccion_basica : int, db : Session = Depends(DataBase.get_db)):
    return CategoriasLogica.categorias_por_periodo_lista(cod_fraccion_basica, db)

@router.delete('/categoria/{cod_categoria}')
def categoria_delete(cod_categoria : int, db : Session = Depends(DataBase.get_db)):
    return CategoriasLogica.categoria_delete(cod_categoria, db)

#? lista categorias por periodo fiscal para mostrar en la lista de comprobantes
@router.get('/categorias_por_anio_lista/{anio}' , response_model=List[CategoriaLista])
def categorias_por_anio_lista(anio : int, db : Session = Depends(DataBase.get_db)):
    return CategoriasLogica.categorias_por_anio_lista(anio, db)

@router.get('/categorias_unicas_get' , response_model=List[CategoriasUnicas])
def categorias_unicas_get( db : Session = Depends(DataBase.get_db)):
    return CategoriasLogica.categorias_unicas_get(db)