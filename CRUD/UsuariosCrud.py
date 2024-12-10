from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import pytz

from Conexion import Config
from Models import Usuarios
from Schemas import UsuarioSchema

# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(ecuador_tz) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UsuarioSchema.UsuarioCreate):
    hashed_password = get_password_hash(user.password)
    db_user = Usuarios.Usuarios(
        identificacion=user.identificacion,
        nombres=user.nombres,
        apellidos=user.apellidos,
        correo=user.correo,
        password=hashed_password,
        tipo_usuario=user.tipo_usuario
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, correo: str):
    return db.query(Usuarios.Usuarios).filter(Usuarios.Usuarios.correo == correo).first()
def get_user_by_identificacion(db: Session, identificacion: str):
    return db.query(Usuarios.Usuarios).filter(Usuarios.Usuarios.identificacion == identificacion).first()