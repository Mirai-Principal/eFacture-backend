import os
from dotenv import load_dotenv

load_dotenv()

# base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

#ENTORNO
ENTORNO = os.getenv("ENTORNO")

# clave publica y pribada para el token de sesion
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH")
 
try:
    with open(PRIVATE_KEY_PATH, "rb") as f:
        PRIVATE_KEY = f.read()

    with open(PUBLIC_KEY_PATH, "rb") as f:
        PUBLIC_KEY = f.read()
except Exception :
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    # Generar clave privada
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Guardar clave privada en un archivo
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Obtener clave pública
    public_key = private_key.public_key()

    # Guardar clave pública en un archivo
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("Claves generadas correctamente.")

    with open(PRIVATE_KEY_PATH, "rb") as f:
        PRIVATE_KEY = f.read()

    with open(PUBLIC_KEY_PATH, "rb") as f:
        PUBLIC_KEY = f.read()
