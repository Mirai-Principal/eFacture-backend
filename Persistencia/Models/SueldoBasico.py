from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SueldoBasico(Base):
    __tablename__ = 'efacture_repo.sueldo_basico'
    cod_sueldo = Column(String, primary_key=True, nullable=False)
    valor_sueldo = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, )
    deleted_at = Column(DateTime, )