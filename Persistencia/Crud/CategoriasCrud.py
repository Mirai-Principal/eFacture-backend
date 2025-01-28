from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import cast, Date, select
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from Persistencia.Models.Categorias import Categorias
from Persistencia.Models.FraccionBasicaDesgravada import FraccionBasicaDesgravada
from Persistencia.Models.PeriodoFiscal import PeriodoFiscal
from Persistencia.Models.Detalles import Detalles

from Schemas import (CategoriasSchema)

class CategoriasCrud:
    def categoria_insert(self, datos : CategoriasSchema.CategoriaCreate, db : Session):
        query = Categorias(
            categoria = datos.categoria,
            descripcion_categoria = datos.descripcion_categoria,
            cod_fraccion_basica = datos.cod_fraccion_basica,
            cant_fraccion_basica = datos.cant_fraccion_basica,
        )
        return self.get_exception(query, "Categoría de comprobante", db)

    def categorias_lista(self, db : Session):
        resultado = db.query(
            Categorias.cod_categoria,
            Categorias.cod_fraccion_basica,
            Categorias.categoria,
            Categorias.descripcion_categoria,
            Categorias.cant_fraccion_basica,
            cast(Categorias.created_at, Date).label("created_at"),
            FraccionBasicaDesgravada.valor_fraccion_basica,
            PeriodoFiscal.periodo_fiscal,
        )\
        .join(FraccionBasicaDesgravada, FraccionBasicaDesgravada.cod_fraccion_basica == Categorias.cod_fraccion_basica)\
        .join(PeriodoFiscal, PeriodoFiscal.cod_periodo_fiscal == FraccionBasicaDesgravada.cod_periodo_fiscal)\
        .order_by(Categorias.cant_fraccion_basica)\
        .all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado

    def categorias_por_periodo_lista(self, cod_fraccion_basica, db : Session):
        # obtiene el dumie
        fraccion_basica_dumie =  db.query(
                    FraccionBasicaDesgravada.cod_fraccion_basica,
                )\
                .join(PeriodoFiscal, PeriodoFiscal.cod_periodo_fiscal == FraccionBasicaDesgravada.cod_periodo_fiscal)\
                .where(PeriodoFiscal.periodo_fiscal == 9999)\
                .first()

        # consulta categorias incluido el dumie
        resultado = db.query(
            Categorias.cod_categoria,
            Categorias.cod_fraccion_basica,
            Categorias.categoria,
            Categorias.descripcion_categoria,
            Categorias.cant_fraccion_basica,
            cast(Categorias.created_at, Date).label("created_at"),
            FraccionBasicaDesgravada.valor_fraccion_basica,
            PeriodoFiscal.periodo_fiscal,
        )\
        .join(FraccionBasicaDesgravada, FraccionBasicaDesgravada.cod_fraccion_basica == Categorias.cod_fraccion_basica)\
        .join(PeriodoFiscal, PeriodoFiscal.cod_periodo_fiscal == FraccionBasicaDesgravada.cod_periodo_fiscal)\
        .where(FraccionBasicaDesgravada.cod_fraccion_basica.in_([cod_fraccion_basica, fraccion_basica_dumie.cod_fraccion_basica]))\
        .order_by(Categorias.cant_fraccion_basica)\
        .all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado

    def categoria_update(self, datos : CategoriasSchema.CategoriaCreate, db : Session):
        resultado = db.query(Categorias).where(Categorias.cod_categoria == datos.cod_categoria).first()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No se encontró la categoría"}
            )
        resultado.categoria = datos.categoria
        resultado.descripcion_categoria = datos.descripcion_categoria
        resultado.cant_fraccion_basica = datos.cant_fraccion_basica
        resultado.cod_fraccion_basica = datos.cod_fraccion_basica
        return self.get_exception(resultado, "Categoría de comprobante", db)
    
    def categoria_find_one(self, cod_categoria, db : Session):
        return db.query(Categorias).where(Categorias.cod_categoria == cod_categoria).first()

    def categoria_delete(self, cod_categoria, db : Session):
        resultado = self.categoria_find_one(cod_categoria, db)
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No se encontró la categoría"}
            )

        tiene_hijos = db.query(
                Detalles,
            )\
            .join(Categorias, Categorias.cod_categoria == Detalles.cod_categoria)\
            .where(Categorias.cod_categoria == cod_categoria)\
            .all()
        # verifica q no tenga hijos al momento de eliminar
        if len(tiene_hijos) == 0:
            try:
                db.delete(resultado)
                db.commit()  # Confirma los cambios en la base de datos
                return JSONResponse(
                    status_code=200,
                    content={"message": "Registro Eliminado"}
                )
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Ocurrio un error {str(e)}") from e
        else:
            raise HTTPException(status_code=500, detail="No se puede eliminar porque está referenciado en otra tabla.")

    def categorias_unicas_get(self, db):
        return db.query(Categorias.categoria).distinct().all()

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