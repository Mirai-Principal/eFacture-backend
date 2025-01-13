from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Float, Text, DateTime, Numeric, CheckConstraint
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class Categorias(Base):
    __tablename__ = 'categorias'
    __table_args__ = (
        CheckConstraint('cant_sueldos_basico >= 1', name="ckc_estado_categori"),
        CheckConstraint("estado IN ('no disponible', 'disponible')", name="ckc_cant_sueldos_basi_categori"),
        {"schema": "efacture_repo"}  # Especifica el esquema como diccionario
    )

    cod_categoria = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    categoria = Column(String(50), nullable=False)
    descripcion_categoria = Column(Text, nullable=True)
    cant_sueldos_basico = Column(Integer, nullable=False)
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
