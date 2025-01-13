from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, ForeignKey, Numeric
# from sqlalchemy.types import Decimal
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')



class Detalles(Base):
    __tablename__ = 'detalles'
    __table_args__ = {"schema": "efacture_repo"}  # Especifica el esquema aquí
    cod_detalle = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    cod_categoria = Column(Integer, ForeignKey("efacture_repo.categorias.cod_categoria"), nullable=False, default=1)
    cod_comprobante = Column(Integer, ForeignKey("efacture_repo.comprobantes.cod_comprobante"), nullable=False)
    descripcion = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10,2), nullable=False)
    precio_total_sin_impuesto = Column(Numeric(10,2), nullable=False)
    impuesto_valor = Column(Numeric(10,2), nullable=False)
    detalle_valor = Column(Numeric(10,2), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deleted_at = Column(DateTime, )