from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')


class Comprador(Base):
    __tablename__ = 'comprador'
    __table_args__ = {"schema": "efacture_repo"}  # Especifica el esquema aquí
    cod_comprador = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    identificacion_comprador = Column(String(13), nullable=False)
    razon_social_comprador = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    # deteled_at = Column(DateTime, nullable=True)