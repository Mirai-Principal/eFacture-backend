from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Float, Text, DateTime, Numeric, CheckConstraint
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class FraccionBasicaDesgravada(Base):
    __tablename__ = 'categorias'
    __table_args__ = (
        CheckConstraint('cant_fraccion_basica >= 0', name="ckc_cant_fraccion_bas_categori"),
        CheckConstraint("estado IN ('no disponible', 'disponible')", name="ckc_estado_categori"),
        {"schema": "efacture_repo"}  # Especifica el esquema como diccionario
    )

    cod_fraccion_basica = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    categoria = Column(String(50), nullable=False)
    descripcion_categoria = Column(Text, nullable=True)
    cant_fraccion_basica = Column(Numeric(6, 3), nullable=False)
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
