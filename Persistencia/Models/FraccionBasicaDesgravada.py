from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Float, Text, DateTime, Numeric, CheckConstraint, ForeignKey
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class FraccionBasicaDesgravada(Base):
    __tablename__ = 'fraccion_basica_desgravada'
    __table_args__ = (
        CheckConstraint('valor_fraccion_basica >= 0', name="ckc_valor_fraccion_ba_fraccion"),
        {"schema": "efacture_repo"}  # Especifica el esquema como diccionario
    )

    cod_fraccion_basica = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    cod_periodo_fiscal = Column(Integer, ForeignKey("efacture_repo.periodo_fiscal.cod_periodo_fiscal"), nullable=False, unique=True)
    valor_fraccion_basica = Column(Numeric(10, 2), nullable=False)
    
    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        primary_key=True,
        default= datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deleted_at = Column(DateTime, nullable=True)
