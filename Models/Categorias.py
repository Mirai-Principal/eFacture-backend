from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Categorias(Base):
    __tablename__ = 'efacture_repo.categorias'
    cod_categoria = Column(String, primary_key=True, nullable=False)
    categoria = Column(String, nullable=False)
    descripcion_categoria = Column(Text, )
    cant_sueldos_basico = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, )
    deleted_at = Column(DateTime, )