from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class Comprobantes(Base):
    __tablename__ = 'comprobantes'
    __table_args__ = {"schema": "efacture_repo"}  # Especifica el esquema aquí
    cod_comprobante = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    cod_comprador = Column(Integer, ForeignKey("efacture_repo.comprador.cod_comprador"), nullable=False)

    archivo = Column(Text, nullable=False)
    clave_acceso = Column(Text, nullable=False, unique=True)
    razon_social = Column(String(100), nullable=False)
    fecha_emision = Column(Date, nullable=False)
    importe_total = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deleted_at = Column(DateTime, )