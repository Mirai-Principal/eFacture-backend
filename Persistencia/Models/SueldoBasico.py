from datetime import datetime
from sqlalchemy.sql import text

from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, CheckConstraint
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class SueldoBasico(Base):
    __tablename__ = 'sueldo_basico'
    __table_args__ = (
        CheckConstraint("valor_sueldo >= 1", name="ckc_valor_sueldo_sueldo_b"),
        CheckConstraint("estado IN ('no disponible', 'disponible')", name="ckc_estado_sueldo_b"),
        {"schema": "efacture_repo"}   # Este esquema se usará en PostgreSQL; en MySQL se ignorará.
    )
    cod_sueldo = Column(Integer, primary_key=True, nullable=False, autoincrement=True) 
    valor_sueldo = Column(Numeric(7, 2), nullable=False)
    periodo_fiscal = Column(Date, nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default="disponible"  # Valor por defecto
    )
    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        primary_key=True,
        default= datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deleted_at = Column(DateTime, nullable=True)
    