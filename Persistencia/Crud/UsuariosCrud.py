from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from sqlalchemy.exc import DataError, IntegrityError
from fastapi.responses import JSONResponse

from fastapi import HTTPException, status

from Persistencia.Models.Usuarios import Usuarios
from Persistencia.Models.UsuarioMembresia import UsuarioMembresia
from Schemas import UsuarioSchema
from Schemas.UsuarioSchema import UsuarioUpdate
class UsuariosCrud:
    def create_user(self, user: UsuarioSchema.UsuarioCreate, db: Session):
        db_user = Usuarios(
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
    
    def clientes_lista(self, db: Session):
        return db.query(
                Usuarios.cod_usuario,
                Usuarios.identificacion,
                Usuarios.nombres,
                Usuarios.apellidos,
                Usuarios.correo,
                cast(Usuarios.created_at, Date).label("created_at"),
                UsuarioMembresia.estado_membresia,
                cast(UsuarioMembresia.fecha_vencimiento, Date).label("fecha_vencimiento"),
                UsuarioMembresia.cant_comprobantes_permitidos,
            )\
            .where(Usuarios.tipo_usuario != 'admin')\
            .join(UsuarioMembresia, UsuarioMembresia.cod_usuario == Usuarios.cod_usuario)\
            .all()

    def get_user_by_email(self, correo: str, db: Session):
        return db.query(Usuarios).filter(Usuarios.correo == correo).first()

    def get_user_by_identificacion(self, identificacion: str, db: Session):
        return db.query(Usuarios).filter(Usuarios.identificacion == identificacion).first()

    def usuario_update(self, datos : UsuarioUpdate, db: Session):
        usuario = self.get_user_by_identificacion(datos.identificacion, db)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        usuario.nombres = datos.nombres
        usuario.apellidos = datos.apellidos
        usuario.correo = datos.correo
        return self.get_exception(usuario, "Ususarios", db)

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

    def get_exception(self, consulta, tabla, db : Session):
        try:
            # Confirmar los cambios en la base de datos
            db.add(consulta)  # Agregar el objeto actualizado al contexto de la sesión
            db.commit()
            db.refresh(consulta)
            return JSONResponse(
                status_code=200,
                content={"message": "Se han guardado los datos"}
            )
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Ya existe una {tabla} con los mismo datos") from e
        except DataError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error de datos: tipos o formato incorrecto") from e
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error interno: datos con formato incorrecto {str(e)}") from e
        return consulta