from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Comprobantes(Base):
    __tablename__ = 'efacture_repo.comprobantes'
    cod_comprobante = Column(String, primary_key=True, nullable=False)
    cod_usuario = Column(String, nullable=False)
    cod_deduccion = Column(String, )
    archivo = Column(Text, nullable=False)
    clave_acceso = Column(Text, nullable=False)
    fecha_comprobante = Column(Date, nullable=False)
    valor = Column(String, nullable=False)
    iva = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, )
    deleted_at = Column(DateTime, )