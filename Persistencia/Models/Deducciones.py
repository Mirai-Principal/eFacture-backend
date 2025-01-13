from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Deducciones(Base):
    __tablename__ = 'efacture_repo.deducciones'
    cod_deduccion = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    prediodo_fiscal = Column(String, nullable=False)
    valor_deducido = Column(String, nullable=False)
    archivo_deduccion = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, )
    updated_at = Column(DateTime, )