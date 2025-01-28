from datetime import timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Persistencia.PersistenciaFacade import AccesoDatosFacade


class CategoriasLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()
    
    def categoria_insert(self, datos, db : Session):
        return self.facade.categoria_insert(datos, db)
    def categorias_lista(self, db : Session):
        return self.facade.categorias_lista(db)
    def categorias_por_periodo_lista(self, cod_fraccion_basica, db : Session):
        return self.facade.categorias_por_periodo_lista(cod_fraccion_basica, db)
    def categorias_por_anio_lista(self, anio, db : Session):
        datos = self.facade.fraccion_basica_find_one_by_periodo(anio, db)
        return self.categorias_por_periodo_lista(datos.cod_fraccion_basica, db)
        
    def categoria_update(self, datos, db : Session):
        return self.facade.categoria_update(datos, db)

    def categoria_delete(self, cod_categoria, db : Session):
        return self.facade.categoria_delete(cod_categoria, db)

    def categorias_unicas_get(self, db : Session):
        return self.facade.categorias_unicas_get(db)