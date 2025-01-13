from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON, CheckConstraint
from datetime import datetime

from Persistencia.Conexion.DataBase import Base


import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class Membresias(Base):
    __tablename__ = 'membresias'
    __table_args__ = (
        CheckConstraint(
            "estado IN ('no disponible', 'disponible')", 
            name="ckc_estado_membresi"
        ),
        {"schema": "efacture_repo"}  # Especifica el esquema como diccionario
    )
    
    cod_membresia = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    nombre_membresia = Column(String, nullable=False)
    descripcion_membresia = Column(String, nullable=False)
    caracteristicas = Column(Text, nullable=False)
    precio = Column(Numeric(5, 2), nullable=False)
    cant_comprobantes_carga = Column(Integer, nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default="no disponible"  # Valor por defecto
    )
    fecha_lanzamiento = Column(DateTime, nullable=False)
    vigencia_meses = Column(Integer, nullable=False)
    fecha_finalizacion = Column(DateTime, nullable=False)
    created_at = Column(
        DateTime, 
        nullable=False, 
        default= datetime.now(ecuador_tz)  # Valor por defecto con zona horaria
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Actualización automática
    )
