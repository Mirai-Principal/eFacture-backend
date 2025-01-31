from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, String
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta
from Persistencia.Conexion.DataBase import Base


import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')


class UsuariosSesion(Base):
    __tablename__ = 'usuarios_sesion'
    __table_args__ = {"schema": "efacture_repo"}  # Especifica el esquema aquí
    
    cod_usuario_sesion = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    cod_usuario = Column(Integer, ForeignKey("efacture_repo.usuarios.cod_usuario"), primary_key=True)
    token_sesion = Column(Text, nullable=True)
    intentos_login = Column(Integer, nullable=False)
    ip_cliente = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    deteled_at = Column(DateTime, nullable=True)