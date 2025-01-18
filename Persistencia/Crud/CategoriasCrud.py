from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import cast, Date
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from Persistencia.Models.Categorias import Categorias
from Persistencia.Models.FraccionBasicaDesgravada import FraccionBasicaDesgravada
from Persistencia.Models.PeriodoFiscal import PeriodoFiscal

from Schemas import (CategoriasSchema)

class CategoriasCrud:
    def categoria_insert(self, datos : CategoriasSchema.CategoriaCreate, db : Session):
        query = Categorias(
            categoria = datos.categoria,
            descripcion_categoria = datos.descripcion_categoria,
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