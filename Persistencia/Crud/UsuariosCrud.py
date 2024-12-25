from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from Logica import Auth
from Persistencia.Models import Usuarios
from Schemas import UsuarioSchema
class UsuariosCrud:
    def create_user(self, user: UsuarioSchema.UsuarioCreate, db: Session):
        db_user = Usuarios.Usuarios(
            identificacion=user.identificacion,
            nombres=user.nombres,
            apellidos=user.apellidos,
            correo=user.correo,
            password=user.password,
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

    def update_password(self, datos : UsuarioSchema.UsuarioUpdatePassword, db: Session):
        # Busca el usuario en la base de datos
        usuario = self.get_user_by_email(datos.correo, db)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        usuario.password = datos.password
        try:
        # Guarda los cambios en la base de datos
            db.commit()
            db.refresh(usuario)
            return {"detail": "Usuario actualizado correctamente"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la actualización") from e