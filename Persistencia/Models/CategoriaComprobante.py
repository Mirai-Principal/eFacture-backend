from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CategoriaComprobante(Base):
    __tablename__ = 'efacture_repo.categoria_comprobante'
    cod_comprobante = Column(String, primary_key=True, nullable=False)
    cod_categoria = Column(String, primary_key=True, nullable=False)
    cod_sueldo = Column(String, )
    valor_categoria = Column(String, nullable=False)
    valor_deducido_cat = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, )
    deleted_at = Column(DateTime, )