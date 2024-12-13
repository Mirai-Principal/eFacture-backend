from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from Persistencia.Conexion import DataBase

from Logica import Auth
from Persistencia.Models import Usuarios
from Persistencia.Schemas import UsuarioSchema


class UsuariosCrud:
    def create_user(self, user: UsuarioSchema.UsuarioCreate, db: Session):
        hashed_password = Auth.get_password_hash(user.password)
        db_user = Usuarios.Usuarios(
            identificacion=user.identificacion,
            nombres=user.nombres,
            apellidos=user.apellidos,
            correo=user.correo,
            password=hashed_password,
            tipo_usuario=user.tipo_usuario
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_email(self, correo: str, db: Session):
        return db.query(Usuarios.Usuarios).filter(Usuarios.Usuarios.correo == correo).first()

    def get_user_by_identificacion(self, identificacion: str, db: Session):
        return db.query(Usuarios.Usuarios).filter(Usuarios.Usuarios.identificacion == identificacion).first()