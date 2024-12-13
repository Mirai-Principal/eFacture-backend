from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Membresias(Base):
    __tablename__ = 'efacture_repo.membresias'
    cod_membresia = Column(String, primary_key=True, nullable=False)
    nombre_membresia = Column(String, nullable=False)
    descripcion_membresia = Column(Text, nullable=False)
    precio = Column(String, nullable=False)
    cant_comprobantes_carga = Column(Integer, nullable=False)
    duracion = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    fecha_lanzamiento = Column(DateTime, nullable=False)
    vigencia_meses = Column(String, nullable=False)
    fecha_finalizacion = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, )
    deleted_at = Column(DateTime, )