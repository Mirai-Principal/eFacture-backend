from datetime import datetime

from sqlalchemy import Column, String, Date, Numeric, Integer, DateTime

from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class DataSetEntrenado(Base):
    __tablename__ = 'dataset_entrenado'
    __table_args__ = {"schema": "efacture_repo"}  # Especifica el esquema aquí

    id = Column(Integer, autoincrement=True, primary_key=True)
    usuario = Column(String(13), nullable=False)
    fecha = Column(Date, nullable=False)
    anio = Column(Integer, nullable=False) 
    mes = Column(Integer, nullable=False)
    categoria = Column(String(50), nullable=False)
    monto = Column(Numeric(10,2), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deleted_at = Column(DateTime, )