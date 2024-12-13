import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

from Persistencia.Conexion import Config

# Cargar variables de entorno
load_dotenv()
EMAIL_HOST=Config.EMAIL_HOST
EMAIL_PORT=Config.EMAIL_PORT
EMAIL_USER=Config.EMAIL_USER
EMAIL_PASSWORD=Config.EMAIL_PASSWORD


def enviar_email(destinatario: str, asunto: str, mensaje: str, archivo_adjunto: str = None):
    """
        para enviar correos
    """
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
