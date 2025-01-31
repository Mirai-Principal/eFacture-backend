from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric

from datetime import datetime, timedelta
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class Configuracion(Base):
    __tablename__ = 'configuracion'
    __table_args__ = {"schema": "efacture_repo"}  # Especifica el esquema aquí
    
    cod_regla = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(Text, nullable=False)
    campo =  Column(String(50), nullable=False)
    operador =  Column(String(20), nullable=False)
    valor = Column(String(50), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deleted_at = Column(DateTime, )