from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Middlewares.JWTMiddleware import OptionsToken

from Persistencia.PersistenciaFacade import AccesoDatosFacade

class UsuarioMembresiaLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()

    def visualizar_mi_suscripcion(self, request : Request, db: Session):
        datos = self.get_info_token(request)
        correo = datos.get("sub")
        usuario_cuenta = self.facade.UsuariosCrud.get_user_by_email(correo, db)
        if not usuario_cuenta:
            return JSONResponse(
                status_code=200,
                content={"message": "Usuario no encontrado"}
            )
        cod_usuario = usuario_cuenta.cod_usuario
        resultado = self.facade.UsuarioMembresiaCrud.visualizar_mi_suscripcion(cod_usuario, db)
        return resultado

    def get_estado_suscripcion(self, request : Request, db : Session):
        datos = self.get_info_token(request)
        correo = datos.get("sub")
        usuario_cuenta = self.facade.UsuariosCrud.get_user_by_email(correo, db)
        cod_usuario = usuario_cuenta.cod_usuario
        resultado = self.facade.UsuarioMembresiaCrud.get_estado_suscripcion(cod_usuario, db)
        return resultado

    def get_info_token(self, request : Request):
        token = request.headers.get("Authorization")
        token = token.split(" ")
        payload = OptionsToken.get_info_token(token[1])
        return payload