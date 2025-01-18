from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Text, DateTime, Numeric, CheckConstraint, ForeignKey
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class AnexoGatosPersonales(Base):
    __tablename__ = 'anexo_gastos_personales'
    __table_args__ = (
        {"schema": "efacture_repo"}  # Especifica el esquema como diccionario
    )

    cod_agp = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    cod_usuario = Column(Integer, ForeignKey("efacture_repo.usuarios.cod_usuario"), nullable=False)
    cod_periodo_fiscal = Column(Integer, ForeignKey("efacture_repo.periodo_fiscal.cod_periodo_fiscal"), nullable=False)
    valor_total_agp = Column(Numeric, nullable=False)
    archivo_agp = Column(Text, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        primary_key=True,
        default= datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deleted_at = Column(DateTime, nullable=True)
