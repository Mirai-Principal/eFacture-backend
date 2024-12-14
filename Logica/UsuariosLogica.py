from fastapi import Depends, HTTPException, Request
from Logica import Auth, Email
from datetime import timedelta
from sqlalchemy.orm import Session

from Persistencia.PersistenciaFacade import AccesoDatosFacade

class UsuariosLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()

    def registrar_usuario(self, user, db: Session):
        correo_existe = self.facade.get_user_by_email(user.correo, db)
        if correo_existe:
            raise HTTPException(status_code=400, detail="Correo ya registrado")
        identificacion_existe = self.facade.get_user_by_identificacion( user.identificacion, db)
        if identificacion_existe:
            raise HTTPException(status_code=400, detail="Identificación ya registrada")
        return self.facade.create_user(user, db)

    def login(self, user, db: Session):
        db_user = self.facade.get_user_by_email(user.correo, db)
        if db_user is None or not Auth.verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        access_token = Auth.create_access_token(data={"sub": db_user.correo})
        return {"access_token": access_token, "token_type": "bearer"}

    def password_reset(self, request: Request, data, db: Session):
        """
        Reiniciar password
        expires_delta = token valido por 5 minutos
        data = recibe el correo
        """

        correo_existe = self.facade.get_user_by_email(data.correo, db)
        if correo_existe:
            token = Auth.create_access_token(data={"sub": data.correo}, expires_delta = timedelta(minutes=10))

            # Obtención del dominio de forma dinámica 
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
                return 'Se te a enviado un correo a tu dirección para que puedas recuperar tu contraseña'
            except Exception as e: 
                # Código que se ejecuta para cualquier otra excepción 
                print(f"Error inesperado: {e}")
                return "No se ha podido enviar el correo de recuración"
        else:
            print("Correo no resgitrado")
            raise HTTPException(status_code=404 , detail="Correo no resgitrado")

    def cambiar_password(self, datos, db: Session):
        datos_token = Auth.verify_token(datos.token)
        datos.correo = datos_token['sub']
        datos.password = Auth.get_password_hash(datos.password)

        return self.facade.update_password(datos, db)
    