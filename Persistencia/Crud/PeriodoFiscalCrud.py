from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import distinct, and_
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from Persistencia.Models.PeriodoFiscal import PeriodoFiscal
from Persistencia.Models.FraccionBasicaDesgravada import FraccionBasicaDesgravada
from Schemas.PeriodoFiscalSchema import (PeriodoFiscalCreate, PeriodoFiscalDetele)

class PeriodoFiscalCrud:
    # para listar en las tablas en la vista
    def periodo_fiscal_lista(self, db : Session):
        resultado = db.query(PeriodoFiscal).order_by(PeriodoFiscal.periodo_fiscal.desc()).all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado
    
    # al listar en eleselct para gesitrar una nueva fraccion basica solo deben aparecer los periodos q no tengas asignar una fraccion basica
    def periodo_fiscal_lista_select(self, db :Session):
        lista_periodo_fiscal = db.query(distinct(FraccionBasicaDesgravada.cod_periodo_fiscal)).all()
        # Extraer los valores de la lista de tuplas
        lista_periodo_fiscal = [item[0] for item in lista_periodo_fiscal]

        resultado = db.query(PeriodoFiscal).order_by(PeriodoFiscal.periodo_fiscal.desc())\
            .where(~PeriodoFiscal.cod_periodo_fiscal.in_(lista_periodo_fiscal))\
            .all()
            
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado

    def periodo_fiscal_find_one(self, cod_periodo_fiscal, db : Session):
        return db.query(PeriodoFiscal).where(PeriodoFiscal.cod_periodo_fiscal == cod_periodo_fiscal).first()
        
    def periodo_fiscal_insert(self, datos : PeriodoFiscalCreate, db : Session):
        query = PeriodoFiscal(
            periodo_fiscal = datos.periodo_fiscal
        )
        return self.get_exception(query, "Periodo Fiscal", db)

    def periodo_fiscal_delete(self, datos : PeriodoFiscalDetele, db : Session):
        resultado = self.periodo_fiscal_find_one(datos.cod_periodo_fiscal, db)
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No se encontró el Periodo Fiscal"}
            )

        tiene_hijos = db.query(
                PeriodoFiscal,
            )\
            .join(FraccionBasicaDesgravada, FraccionBasicaDesgravada.cod_periodo_fiscal == PeriodoFiscal.cod_periodo_fiscal)\
            .where(PeriodoFiscal.cod_periodo_fiscal == datos.cod_periodo_fiscal)\
            .all()

        # verifica q no tenga hijos al momento de eliminar
        if len(tiene_hijos) == 0:
            try:
                db.delete(resultado)
                db.commit()  # Confirma los cambios en la base de datos
                return self.periodo_fiscal_lista(db)
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Ocurrio un error {str(e)}") from e
        else:
            raise HTTPException(status_code=500, detail="No se puede eliminar porque está referenciado en otra tabla.")

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