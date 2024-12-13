from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, DateTime, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UsuarioMembresia(Base):
    __tablename__ = 'efacture_repo.usuario_membresia'
    cod_usuario = Column(String, primary_key=True, nullable=False)
    cod_membresia = Column(String, primary_key=True, nullable=False)
    estado_membresia = Column(String, nullable=False)
    created_at = Column(DateTime, primary_key=True, nullable=False)
    updated_at = Column(DateTime, )
    deleted_at = Column(DateTime, )