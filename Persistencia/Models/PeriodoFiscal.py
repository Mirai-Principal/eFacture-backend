
from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Float, Text, DateTime, Numeric, CheckConstraint
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class PeriodoFiscal(Base):
    __tablename__ = 'periodo_fiscal'
    __table_args__ = (
        CheckConstraint('periodo_fiscal >= 2021', name="ckc_periodo_fiscal_periodo_"),
        {"schema": "efacture_repo"}  # Especifica el esquema como diccionario
    )

    cod_periodo_fiscal = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    periodo_fiscal = Column(Numeric(4), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        primary_key=True,
        default= datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deleted_at = Column(DateTime, nullable=True)
