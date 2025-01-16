from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from Persistencia.Models.Categorias import Categorias
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
        resultado = db.query(Categorias).all()
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
        resultado.fraccion_basica_desgravada = datos.fraccion_basica_desgravada
        resultado.estado = datos.estado
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