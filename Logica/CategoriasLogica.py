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
    def categoria_update(self, datos, db : Session):
        return self.facade.categoria_update(datos, db)