from datetime import timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Logica import Auth, Email

from Persistencia.PersistenciaFacade import AccesoDatosFacade

class UsuarioMembresiaLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()

    def visualizar_mi_suscripcion(self, db: Session):
        resultado = self.facade.visualizar_mi_suscripcion(db)
        return resultado