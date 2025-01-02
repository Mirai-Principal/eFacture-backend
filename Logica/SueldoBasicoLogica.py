from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Persistencia.PersistenciaFacade import AccesoDatosFacade

class SueldoBasicoLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()

    def sueldo_basico_insert(self, datos, db : Session):
        return self.facade.sueldo_basico_insert(datos, db)

    def lista_sueldo_basico(self, db : Session):
        return self.facade.lista_sueldo_basico(db)