from datetime import timedelta, datetime

from fastapi import  HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Logica import Auth, Email

from Persistencia.PersistenciaFacade import AccesoDatosFacade
from Middlewares.JWTMiddleware import OptionsToken

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

import operator
# Diccionario que mapea operadores a funciones
OPERATORS = {
    '=': operator.eq,
    '==': operator.eq,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '!=': operator.ne,
    'in': lambda x, y: x in y,  # Soporte para "in"
    'between': lambda x, y: y[0] <= x <= y[1],  # Soporte para rangos
}

class UsuariosLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()

    def registrar_usuario(self, user, db: Session):
        correo_existe = self.facade.get_user_by_email(user.correo, db)
        if correo_existe:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Correo ya registrado")
        identificacion_existe = self.facade.get_user_by_identificacion( user.identificacion, db)
        if identificacion_existe:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identificación ya registrada")

        user.password = Auth.get_password_hash(user.password)
        return self.facade.create_user(user, db)

    def login(self, request: Request, user, db: Session):
        db_user = self.facade.UsuariosCrud.get_user_by_email(user.correo, db)

        client_host = request.client.host  # Esto devuelve la IP del cliente

        regla_intentos = self.facade.ConfiguracionCrud.configuracion_get_by_nombre("intentos_login", db)
        #! Obtener la función del operador   
        operation_regla_intentos = OPERATORS.get(regla_intentos.operador)

        regla_tiempo = self.facade.ConfiguracionCrud.configuracion_get_by_nombre("tiempo_bloqueo_login", db)
        operadoer_regla_tiempo = OPERATORS.get(regla_tiempo.operador)

        now = datetime.now()

        if db_user is None or not Auth.verify_password(user.password, db_user.password):
            #? Obtener la IP del cliente desde los encabezados
            usuario_sesion = self.facade.UsuariosSesionCrud.usuario_session_find_one(db_user.cod_usuario, client_host, db)
#             Si el servidor está detrás de un proxy o un balanceador de carga (como Nginx), la IP que obtendrás será la del proxy.
            # Para obtener la IP real del cliente, revisa el encabezado X-Forwarded-For
            # Intenta obtener la IP del cliente desde el encabezado 'X-Forwarded-For'
            # forwarded_for = request.headers.get("X-Forwarded-For")
            # client_ip = forwarded_for.split(",")[0] if forwarded_for else request.client.host

            if not usuario_sesion:
                self.facade.UsuariosSesionCrud.usuario_session_create(db_user.cod_usuario, client_host, db)
            else:
                
                # Calcular si han pasado N minutos
                #! evalua la condicion de la regla
                if operadoer_regla_tiempo(now - usuario_sesion.updated_at, timedelta(minutes = int(regla_tiempo.valor))):
                    self.facade.UsuariosSesionCrud.usuario_session_delete(db_user.cod_usuario, client_host, db)
                else:
                    if operation_regla_intentos(usuario_sesion.intentos_login, int(regla_intentos.valor)):
                        tiempo_restante = timedelta(minutes=int(regla_tiempo.valor)) - (now - usuario_sesion.updated_at)
                        tiempo_restante = str(tiempo_restante).split('.')[0][2:]
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Usuario bloqueado por {tiempo_restante} minutos")
                    else:
                        self.facade.UsuariosSesionCrud.usuario_session_update(db_user.cod_usuario, client_host, db)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
        else:
            usuario_sesion = self.facade.UsuariosSesionCrud.usuario_session_find_one(db_user.cod_usuario, client_host, db)
            if not usuario_sesion or usuario_sesion.intentos_login < int(regla_intentos.valor):
                if usuario_sesion:
                    self.facade.UsuariosSesionCrud.usuario_session_delete(db_user.cod_usuario, client_host, db) 

                access_token = OptionsToken.create_access_token(data={"sub": db_user.correo, "tipo_usuario": db_user.tipo_usuario})
                response = JSONResponse(content={"tipo_usuario": db_user.tipo_usuario})

                response.headers["Authorization"] = f"Bearer {access_token}"
                response.headers["sub"] = db_user.correo
                response.headers["tipo_usuario"] = db_user.tipo_usuario
                return response
            else:
                
                # Calcular si han pasado N minutos
                #! evalua la condicion de la regla
                if operadoer_regla_tiempo(now - usuario_sesion.updated_at, timedelta(minutes = int(regla_tiempo.valor))):
                    self.facade.UsuariosSesionCrud.usuario_session_delete(db_user.cod_usuario, client_host, db)
                else:
                    if operation_regla_intentos(usuario_sesion.intentos_login, int(regla_intentos.valor)):
                        tiempo_restante = timedelta(minutes=int(regla_tiempo.valor)) - (now - usuario_sesion.updated_at)
                        tiempo_restante = str(tiempo_restante).split('.')[0][2:]
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Usuario bloqueado por {tiempo_restante} minutos")
                    else:
                        self.facade.UsuariosSesionCrud.usuario_session_update(db_user.cod_usuario, client_host, db)
            
               

    def password_reset(self, request: Request, data, db: Session):
        """
        Reiniciar password
        expires_delta = token valido por 10 minutos
        data = recibe el correo
        """

        correo_existe = self.facade.get_user_by_email(data.correo, db)
        if correo_existe:
            token = OptionsToken.create_access_token({"sub": data.correo, "tipo_usuario": correo_existe.tipo_usuario }, 10)

            #? Obtención del dominio de forma dinámica 
            origin = request.headers.get("origin")
            reset_link = f"{origin}/cambiar_password?k={token}"

            # request_dict = request.__dict__ 
            # print(request_dict)

            try:
                Email.enviar_email(
                destinatario=data.correo,
                asunto="Recuperar contraseña",
                mensaje="<!DOCTYPE html> <html lang='es'> <head> <meta charset='UTF-8'> <meta name='viewport' content='width=device-width, initial-scale=1.0'> <title>Recuperación de Contraseña</title> <style> body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; } .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); } .header { background-color: #4CAF50; color: white; padding: 10px 0; text-align: center; } .content { padding: 20px; text-align: center; } .button { background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; } .footer { text-align: center; padding: 20px; font-size: 12px; color: #777; } </style> </head> <body> <div class='container'> <div class='header'> <h1>Recuperación de Contraseña</h1> </div> <div class='content'> <p>Hola,</p> <p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta. Si no realizaste esta solicitud, puedes ignorar este correo.</p> <p>Para restablecer tu contraseña, haz clic en el siguiente enlace:</p> <a href='" + reset_link + "' class='button'>Restablecer Contraseña</a> <p>Link valido por 10 minutos</p> <p>Si tienes algún problema, por favor, contáctanos.</p> <p>Correo: soporte@efacture.com</p> </div> <div class='footer'> <p>© 2024 eFacure - SMARTWARE. Todos los derechos reservados.</p> </div> </div> </body></html>",
                archivo_adjunto=None  # Cambia esto si quieres adjuntar un archivo
                )
                return {"detail": "Se te a enviado un correo a tu dirección para que puedas recuperar tu contraseña"}
            except Exception as e: 
                # Código que se ejecuta para cualquier otra excepción 
                print(f"Error inesperado: {e}")
                raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="No se ha podido enviar el correo de recuración") from e

        else:
            print("Correo no resgitrado")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Correo no resgitrado")

    def cambiar_password(self, token: str, datos, db: Session):
        payload = OptionsToken.get_info_token(token)
        datos.correo = payload.get("sub")
        datos.password = Auth.get_password_hash(datos.password)
        return self.facade.update_password(datos, db)
        
    def clientes_lista(self, db: Session):
        return self.facade.UsuariosCrud.clientes_lista(db)    
    
    def usuario_update(self, datos, db: Session):
        return self.facade.UsuariosCrud.usuario_update(datos, db)

    def usuario_by_correo(self, request : Request, db: Session):
        token = request.headers.get("Authorization")
        token = token.split(" ")
        payload = OptionsToken.get_info_token(token[1])
        correo = payload.get("sub")
        usuario_cuenta = self.facade.UsuariosCrud.get_user_by_email(correo, db)
        if not usuario_cuenta:
            return JSONResponse(
                status_code=200,
                content={"message": "Usuario no encontrado"}
            )
        return usuario_cuenta



        