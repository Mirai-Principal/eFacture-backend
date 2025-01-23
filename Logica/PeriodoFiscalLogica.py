from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Persistencia.PersistenciaFacade import AccesoDatosFacade

class PeriodoFiscal:
    def __init__(self):
        self.facade = AccesoDatosFacade()

    def periodo_fiscal_insert(self, datos, db : Session):
        return self.facade.periodo_fiscal_insert(datos, db)

    def periodo_fiscal_lista_select(self, db :Session):
        return self.facade.periodo_fiscal_lista_select(db)
        
    def periodo_fiscal_lista(self, db : Session):
        return self.facade.periodo_fiscal_lista(db)
    def periodo_fiscal_delete(self, datos, db : Session):
        return self.facade.periodo_fiscal_delete(datos, db)