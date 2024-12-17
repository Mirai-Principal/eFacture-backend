from fastapi import Depends, HTTPException, Request
from Logica import Auth, Email
from datetime import timedelta
from sqlalchemy.orm import Session

from Persistencia.PersistenciaFacade import AccesoDatosFacade

class MembresiasLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()
    
    def lista_membresias(self, db : Session):
        membresias = self.facade.lista_membresias(db)
        if not membresias:
            raise HTTPException(status_code=404, detail="No se encontraron membresías")
        return membresias
    def nueva_membresia(self, datos, db : Session):
        return self.facade.nueva_membresia(datos, db)

    def actualizar_membresia(self, datos, db : Session):
        return self.facade.actualizar_membresia(datos, db)

    def visualizar_membresia(self, cod, db : Session):
        return self.facade.visualizar_membresia(cod, db)