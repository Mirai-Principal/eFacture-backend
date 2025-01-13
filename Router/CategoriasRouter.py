from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from Logica.CategoriasLogica import CategoriasLogica
from Schemas.CategoriasSchema import CategoriaCreate, CategoriaLista

from Persistencia.Conexion import DataBase

router = APIRouter()
CategoriasLogica = CategoriasLogica()

@router.post('/categorias_insert')
def categorias_insert( datos : CategoriaCreate, db : Session = Depends(DataBase.get_db)):
    if datos.cod_categoria - 0:
        return CategoriasLogica.categoria_update(datos, db)
    return CategoriasLogica.categoria_insert(datos, db)

@router.get('/categorias_lista' , response_model=List[CategoriaLista])
def categorias_lista(db : Session = Depends(DataBase.get_db)):
    return CategoriasLogica.categorias_lista(db)