from sqlalchemy import (
    Column, String, Text, Integer, DateTime, ForeignKey, CheckConstraint, Numeric, Date
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Categoria(Base):
    __tablename__ = "categorias"
    __table_args__ = (
        CheckConstraint('cant_sueldos_basico >= 1', name="ckc_cant_sueldos_basi_categori"),
    )

    cod_categoria = Column(String(10), primary_key=True, default=func.concat("cat_", func.nextval("efacture_repo.sq_categorias")))
    categoria = Column(String(50), nullable=False, unique=True)
    descripcion_categoria = Column(Text)
    cant_sueldos_basico = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        CheckConstraint("tipo_usuario IN ('cliente', 'admin')", name="ckc_tipo_usuario_usuarios"),
    )

    cod_usuario = Column(String(10), primary_key=True, default=func.concat("usu_", func.nextval("efacture_repo.sq_usuarios")))
    identificacion = Column(String(13), nullable=False, unique=True)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    tipo_usuario = Column(String(20), nullable=False, default="cliente")
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime)
    deteled_at = Column(DateTime)


class Deduccion(Base):
    __tablename__ = "deducciones"

    cod_deduccion = Column(String(10), primary_key=True, default=func.concat("ded_", func.nextval("efacture_repo.sq_deducciones")))
    prediodo_fiscal = Column(String(50), nullable=False)
    valor_deducido = Column(Numeric(10, 2), nullable=False)
    archivo_deduccion = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class Comprobante(Base):
    __tablename__ = "comprobantes"

    cod_comprobante = Column(String(10), primary_key=True, default=func.concat("com_", func.nextval("efacture_repo.sq_comprobantes")))
    cod_usuario = Column(String(10), ForeignKey("usuarios.cod_usuario"), nullable=False)
    cod_deduccion = Column(String(10), ForeignKey("deducciones.cod_deduccion"))
    archivo = Column(Text, nullable=False)
    clave_acceso = Column(Text, nullable=False, unique=True)
    fecha_comprobante = Column(Date, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    iva = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    usuario = relationship("Usuario", back_populates="comprobantes")
    deduccion = relationship("Deduccion", back_populates="comprobantes")


class SueldoBasico(Base):
    __tablename__ = "sueldo_basico"
    __table_args__ = (
        CheckConstraint("valor_sueldo >= 1", name="ckc_valor_sueldo_sueldo_b"),
    )

    cod_sueldo = Column(String(10), primary_key=True, default=func.concat("sbu_", func.nextval("efacture_repo.sq_sueldo_basico")))
    valor_sueldo = Column(Numeric(10, 2), nullable=False, default=460)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class CategoriaComprobante(Base):
    __tablename__ = "categoria_comprobante"

    cod_comprobante = Column(String(10), ForeignKey("comprobantes.cod_comprobante"), primary_key=True)
    cod_categoria = Column(String(10), ForeignKey("categorias.cod_categoria"), primary_key=True)
    cod_sueldo = Column(String(10), ForeignKey("sueldo_basico.cod_sueldo"))
    valor_categoria = Column(Numeric(10, 2), nullable=False)
    valor_deducido_cat = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class Membresia(Base):
    __tablename__ = "membresias"
    __table_args__ = (
        CheckConstraint("estado IN ('no disponible', 'disponible')", name="ckc_estado_membresi"),
        CheckConstraint("vigencia_meses >= 1", name="ckc_vigencia_meses_membresi"),
        CheckConstraint("destacado IN ('si', 'no')", name="ckc_destacado_membresi"),
    )

    cod_membresia = Column(String(10), primary_key=True, default=func.concat("mem_", func.nextval("efacture_repo.sq_membresias")))
    nombre_membresia = Column(String(50), nullable=False)
    descripcion_membresia = Column(Text, nullable=False)
    caracterisicas = Column(Text, nullable=False)
    precio = Column(Numeric(5, 2), nullable=False)
    cant_comprobantes_carga = Column(Integer, nullable=False)
    estado = Column(String(20), nullable=False, default="no disponible")
    fecha_lanzamiento = Column(Date, nullable=False)
    vigencia_meses = Column(Integer, nullable=False, default=12)
    fecha_finalizacion = Column(Date, nullable=False)
    destacado = Column(String(2), nullable=False, default="no")
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class UsuarioMembresia(Base):
    __tablename__ = "usuario_membresia"

    cod_usuario = Column(String(10), ForeignKey("usuarios.cod_usuario"), primary_key=True)
    cod_membresia = Column(String(10), ForeignKey("membresias.cod_membresia"), primary_key=True)
    order_id_paypal = Column(String(50), nullable=False)
    estado_membresia = Column(String(20), nullable=False, default="vigente")
    created_at = Column(DateTime, primary_key=True, default=func.current_timestamp())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
