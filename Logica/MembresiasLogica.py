from datetime import timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Logica import Auth, Email
from Persistencia.Conexion import Config

from Persistencia.PersistenciaFacade import AccesoDatosFacade
from Middlewares.JWTMiddleware import OptionsToken


class MembresiasLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()
    
    def lista_membresias(self, db : Session):
        membresias = self.facade.lista_membresias(db)
        # Retorna un valor por defecto si no hay filas
        if not membresias:
            return JSONResponse(
                status_code=200,
                content={"message": "No se encontraron membresías registradas"}
            )
        return membresias
    
    def lista_memb_disponibles(self, db : Session):
        membresias = self.facade.lista_memb_disponibles(db)
        if not membresias:
            raise HTTPException(status_code=200, detail="No se encontraron membresías disponibles")
        return membresias

    def nueva_membresia(self, datos, db : Session):
        return self.facade.nueva_membresia(datos, db)

    def actualizar_membresia(self, datos, db : Session):
        return self.facade.actualizar_membresia(datos, db)

    def visualizar_membresia(self, cod, db : Session):
        return self.facade.visualizar_membresia(cod, db)

    def generar_suscripcion(self, token : str, datos, db : Session):
        # obtener cod_usuario
        payload = OptionsToken.get_info_token(token)
        correo = payload.get("sub")
        usuario = self.facade.get_user_by_email(correo, db)

        datos.cod_usuario = usuario.cod_usuario
        datos.estado_membresia = "vigente"

        membresia = self.visualizar_membresia(datos.cod_membresia, db)
        if float(membresia.precio) == float(datos.precio):
            try:
                return self.facade.generar_suscripcion(datos, db)
            except Exception as e:
                 raise HTTPException(status_code=400, detail=str(e)) from e
        else:
            raise HTTPException(status_code=400, detail="Error de datos: el valor pagado no es igual al valor del plan")