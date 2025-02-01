from datetime import timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Persistencia.PersistenciaFacade import AccesoDatosFacade

class ConfiguracionLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()
    
    def configuracion_get_by_id(self, cod_regla : int, db : Session):
        return self.facade.ConfiguracionCrud.configuracion_get_by_id(cod_regla, db) 
    
    def configuracion_lista(self, db : Session):
        return self.facade.ConfiguracionCrud.configuracion_lista(db)

    def configuracion_get_by_nombre(self, nombre : str, db : Session):
        return self.facade.ConfiguracionCrud.configuracion_get_by_nombre(nombre, db)

    def configuracion_update(self, datos, db : Session):
        return self.facade.ConfiguracionCrud.configuracion_update(datos, db)
