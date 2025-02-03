import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from sqlalchemy.orm import Session

from Logica.Decoradores import Singleton

from Persistencia.PersistenciaFacade import AccesoDatosFacade

@Singleton
class Email:
    def __init__(self):
        self.facade = AccesoDatosFacade()
    

    def enviar_email(self, db : Session, destinatario: str, asunto: str, mensaje: str, archivo_adjunto: str = None):
        """
            para enviar correos
        """
        regla_EMAIL_HOST = self.facade.ConfiguracionCrud.configuracion_get_by_nombre("EMAIL_HOST", db)
        EMAIL_HOST = regla_EMAIL_HOST.valor
        regla_EMAIL_PORT = self.facade.ConfiguracionCrud.configuracion_get_by_nombre("EMAIL_PORT", db)
        EMAIL_PORT = regla_EMAIL_PORT.valor
        regla_EMAIL_USER = self.facade.ConfiguracionCrud.configuracion_get_by_nombre("EMAIL_USER", db)
        EMAIL_USER = regla_EMAIL_USER.valor
        regla_EMAIL_PASSWORD = self.facade.ConfiguracionCrud.configuracion_get_by_nombre("EMAIL_PASSWORD", db)
        EMAIL_PASSWORD = regla_EMAIL_PASSWORD.valor

        try:
            # Crear el mensaje
            msg = MIMEMultipart()
            msg["From"] = EMAIL_USER
            msg["To"] = destinatario
            msg["Subject"] = asunto

            # Agregar el contenido del correo
            msg.attach(MIMEText(mensaje, "html"))

            # Adjuntar archivo (opcional)
            if archivo_adjunto:
                with open(archivo_adjunto, "rb") as file:
                    adjunto = MIMEApplication(file.read(), Name=os.path.basename(archivo_adjunto))
                    adjunto["Content-Disposition"] = f'attachment; filename="{os.path.basename(archivo_adjunto)}"'
                    msg.attach(adjunto)

            # Conexión con el servidor SMTP
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()  # Inicia la conexión segura
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_USER, destinatario, msg.as_string())

            print("Correo enviado exitosamente.")

        except Exception as e:
            print(f"Error al enviar el correo: {e}")

    # # Ejemplo de uso
    # enviar_email(
    #     destinatario="tidomar@gmail.com",
    #     asunto="Hola desde FastAPI",
    #     mensaje="Este es un correo de prueba enviado desde el backend.",
    #     archivo_adjunto=None  # Cambia esto si quieres adjuntar un archivo
    # )
