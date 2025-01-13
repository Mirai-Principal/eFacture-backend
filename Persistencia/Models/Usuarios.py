from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta
from sqlalchemy.sql import text
from Persistencia.Conexion.DataBase import Base


import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')


class Usuarios(Base):
    __tablename__ = 'usuarios'
    __table_args__ = {"schema": "efacture_repo"}  # Especifica el esquema aquí
    cod_usuario = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    identificacion = Column(String, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    password = Column(String, nullable=False)
    tipo_usuario = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deteled_at = Column(DateTime, nullable=True)