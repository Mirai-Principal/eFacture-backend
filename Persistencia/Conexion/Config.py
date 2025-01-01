import os
from dotenv import load_dotenv

load_dotenv()

# base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# correo
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

#ENTORNO
ENTORNO = os.getenv("ENTORNO")

# PAYPAL
MODE = os.getenv("MODE")
if MODE == "sandbox":
    CLIENT_ID = os.getenv("CLIENT_ID_SANDBOX")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET_SANDBOX")
else:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")