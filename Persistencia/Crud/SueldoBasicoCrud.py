from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from Persistencia.Models.SueldoBasico import SueldoBasico
from Schemas import (SueldoBasicoSchema)

class SueldoBasicoCrud:
    def lista_sueldo_basico(self, db : Session):
        resultado = db.query(SueldoBasico).all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado
        
    def sueldo_basico_insert(self, datos : SueldoBasicoSchema.SueldoBasicoCreate, db : Session):
        query = SueldoBasico(
            valor_sueldo = datos.valor_sueldo,
            periodo_fiscal = datos.periodo_fiscal
        )
        return self.get_exception(query, "Sueldo Básico", db)

    def sueldo_basico_update(self, datos : SueldoBasicoSchema.SueldoBasicoCreate, db : Session):
        resultado = db.query(SueldoBasico).where(SueldoBasico.cod_sueldo == datos.cod_sueldo).first()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No se encontró la categoría"}
            )
        resultado.valor_sueldo = datos.valor_sueldo
        resultado.periodo_fiscal = datos.periodo_fiscal
        resultado.estado = datos.estado
        return self.get_exception(resultado, "Sueldo basico", db)

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