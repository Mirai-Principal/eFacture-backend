from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import cast, Date, select, and_
from fastapi import HTTPException
from fastapi.responses import JSONResponse


from Persistencia.Models.UsuariosSesion import UsuariosSesion
from Persistencia.Models.Usuarios import Usuarios

from Schemas.UsuariosSesionSchema import UsuariosSesionCreate, UsuariosSesionUpdate

class UsuariosSesionCrud:
    def usuario_session_find_one(self, cod_usuario : int, ip_cliente : str, db: Session):
        return db.query(UsuariosSesion).where(
            and_(
                UsuariosSesion.cod_usuario == cod_usuario,
                UsuariosSesion.ip_cliente == ip_cliente,
            )
        ).first()


    def usuario_session_create(self, cod_usuario : int, ip_cliente : str, db: Session):
        query = UsuariosSesion(
            cod_usuario = cod_usuario,
            intentos_login = 1,
            ip_cliente = ip_cliente
        )
        return self.get_exception(query, "Usuario sesión", db)
        

    # desbloaquear_usuario 
    def usuario_session_update(self, cod_usuario, ip_cliente, db: Session):
        usuario = self.usuario_session_find_one(cod_usuario, ip_cliente, db)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        usuario.intentos_login += 1
        return self.get_exception(usuario, "Usuario sesión", db)

    def usuario_session_delete(self, cod_usuario, ip_cliente, db: Session):
        usuario = self.usuario_session_find_one(cod_usuario, ip_cliente, db)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        db.delete(usuario)
        db.commit()
        

    def get_exception(self, consulta, tabla, db : Session):
        try:
            # Confirmar los cambios en la base de datos
            db.add(consulta)  # Agregar el objeto actualizado al contexto de la sesión
            db.commit()
            db.refresh(consulta)
            return consulta
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