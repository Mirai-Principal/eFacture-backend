from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import select
from sqlalchemy import cast, Date
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from Persistencia.Models.FraccionBasicaDesgravada import FraccionBasicaDesgravada
from Persistencia.Models.PeriodoFiscal import PeriodoFiscal
from Schemas.FraccionBasicaSchema import (FraccionBasicaCreate, FraccionBasicaDelete)

class FraccionBasicaCrud:
    def fraccion_basica_insert(self, datos : FraccionBasicaCreate, db : Session):
        query = FraccionBasicaDesgravada(
            cod_periodo_fiscal = datos.cod_periodo_fiscal,
            valor_fraccion_basica = datos.valor_fraccion_basica
        )
        return self.get_exception(query, "Fracción Básica Desgravada", db)
    
    def fraccion_basica_list(self, db : Session):
        stmt = (
                select(
                    FraccionBasicaDesgravada.cod_fraccion_basica,
                    FraccionBasicaDesgravada.cod_periodo_fiscal,
                    FraccionBasicaDesgravada.valor_fraccion_basica,
                    PeriodoFiscal.periodo_fiscal,
                    cast(FraccionBasicaDesgravada.created_at.label("created_at"), Date),
                )
                .join(
                    FraccionBasicaDesgravada,
                    PeriodoFiscal.cod_periodo_fiscal == FraccionBasicaDesgravada.cod_periodo_fiscal,
                )
                .order_by(PeriodoFiscal.periodo_fiscal.desc())
             
        )

        # Ejecutar la consulta y obtener resultados como diccionarios
        resultado = db.execute(stmt).mappings().all()
        
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado
    
    def fraccion_basica_find_one(self, cod_fraccion_basica, db : Session):
        return db.query(FraccionBasicaDesgravada).where(FraccionBasicaDesgravada.cod_fraccion_basica == cod_fraccion_basica).first()


    def fraccion_basica_delete(self, datos : FraccionBasicaDelete, db : Session):
        resultado = self.fraccion_basica_find_one(datos.cod_fraccion_basica, db)
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No se encontró la Fracción Básica Desgravada"}
            )
        try:
            db.delete(resultado)
            db.commit()  # Confirma los cambios en la base de datos
            return self.fraccion_basica_list(db)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Ocurrio un error {str(e)}") from e


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