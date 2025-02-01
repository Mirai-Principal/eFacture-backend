from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import cast, Date, select
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from Persistencia.Models.Configuracion import Configuracion 

from Schemas.ConfiguracionSchema import ConfiguracionUpdate 

class ConfiguracionCrud:
    def configuracion_get_by_id(self, cod_regla : int, db : Session):
        resultado = db.query(Configuracion).where(Configuracion.cod_regla == cod_regla).first()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado

    def configuracion_lista(self, db : Session):
        resultado = db.query(Configuracion).order_by(Configuracion.nombre).all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado

    def configuracion_get_by_nombre(self, campo : str, db : Session):
        resultado = db.query(
            Configuracion.nombre,
            Configuracion.operador,
            Configuracion.valor,
            ).where(Configuracion.campo == campo).first()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado

    def configuracion_update(self, datos : ConfiguracionUpdate, db : Session):
        query = db.query(Configuracion).where(Configuracion.cod_regla == datos.cod_regla).first()
        if not query:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        query.nombre = datos.nombre
        query.descripcion = datos.descripcion
        query.operador = datos.operador
        query.valor = datos.valor
        return self.get_exception(query, "Configuración", db)

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