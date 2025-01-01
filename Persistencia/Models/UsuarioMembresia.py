from datetime import datetime, timedelta

from sqlalchemy import Column, String, DateTime, ForeignKey
from Persistencia.Conexion.DataBase import Base

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class UsuarioMembresia(Base):
    __tablename__ = "usuario_membresia"
    __table_args__ = {"schema": "efacture_repo"}  # Especifica el esquema aquí
    cod_usuario = Column(String(10), ForeignKey("efacture_repo.usuarios.cod_usuario"), primary_key=True)
    cod_membresia = Column(String(10), ForeignKey("efacture_repo.membresias.cod_membresia"), primary_key=True)
    order_id_paypal = Column(String(50), nullable=False, primary_key=True)
    estado_membresia = Column(String(20), nullable=False, default="vigente")
    fecha_vencimiento = Column(DateTime, default= datetime.now(ecuador_tz) + timedelta(days=365))
    created_at = Column(DateTime, nullable=False, default=datetime.now(ecuador_tz))
    updated_at = Column(
        DateTime,
        nullable=False,
        primary_key=True,
        default= datetime.now(ecuador_tz),  # Valor inicial
        onupdate=lambda: datetime.now(ecuador_tz)  # Valor al actualizar
    )
    # deteled_at = Column(DateTime, nullable=True)