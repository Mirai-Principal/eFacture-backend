from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import cast, Date, text, select, and_, func, union_all, extract

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from typing import List

from Persistencia.Models.Comprador import Comprador
from Persistencia.Models.Comprobantes import Comprobantes
from Persistencia.Models.Detalles import Detalles 
from Persistencia.Models.Categorias import Categorias 
from Persistencia.Models.DataSetEntrenamiento import DataSetEntrenamiento 
from Persistencia.Models.DataSetEntrenado import DataSetEntrenado 

from Schemas.PrediccionSchema import (DatasetEntrenamientoCreate)
class PrediccionCrud:
    def generar_dataset(self, db: Session):
        resultado = db.query(
            Comprador.identificacion_comprador.label("usuario"),
            Comprobantes.fecha_emision.label("fecha"),
            Categorias.categoria.label("categoria"),
            Detalles.detalle_valor.label("monto")
        )\
        .join(Comprobantes, Comprobantes.cod_comprador == Comprador.cod_comprador)\
        .join(Detalles, Detalles.cod_comprobante == Comprobantes.cod_comprobante)\
        .join(Categorias, Categorias.cod_categoria == Detalles.cod_categoria)\
        .order_by(Comprobantes.fecha_emision)\
        .all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return self.guardar_dataset_entrenamiento(resultado, db)
    
    def guardar_dataset_entrenamiento(self, datos: List[DatasetEntrenamientoCreate], db: Session):
        # Ejecutar el TRUNCATE
        db.execute(text("TRUNCATE TABLE efacture_repo.dataset_entrenamiento"))
        db.commit() 
         # Convertir la lista de objetos a una lista de diccionarios
        data_to_insert = [
            {
                "usuario": dato.usuario,
                "fecha": dato.fecha,
                "categoria": dato.categoria,
                "monto": dato.monto
            }
            for dato in datos
        ]

        try:
            # Confirmar los cambios en la base de datos
            # Insertar en batch usando `bulk_insert_mappings`
            db.bulk_insert_mappings(DataSetEntrenamiento ,data_to_insert) 
            db.commit()
            return self.dataset_entrenamiento_get_all(db)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Ocurrion un error: {str(e)}") from e

    def dataset_entrenamiento_get_all(self, db : Session):
        stmt = (
                select(
                    DataSetEntrenamiento.usuario,
                    DataSetEntrenamiento.fecha,
                    DataSetEntrenamiento.categoria,
                    DataSetEntrenamiento.monto,
                )
            )
        # Ejecutar la consulta y obtener resultados como diccionarios
        return  db.execute(stmt).mappings().all()
        
    def dataset_entrenado_insert(self, datos, db : Session):
        # Ejecutar el TRUNCATE
        db.execute(text("TRUNCATE TABLE efacture_repo.dataset_entrenado"))
        # Usar bulk_insert_mappings para insertar de manera eficiente
        try:
            db.bulk_insert_mappings(DataSetEntrenado, datos)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ocurrion un error: {str(e)}") from e

#? MENSUAL

    def consultar_prediccion(self, usuario, categoria, db : Session):
        resultado = db.query(DataSetEntrenado)\
            .where(
                and_(
                    DataSetEntrenado.usuario == usuario,
                    DataSetEntrenado.categoria == categoria,
                )
            )\
            .all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos para mostrar"}
            )
        return resultado
    
    def consultar_historico(self, usuario, categoria, db: Session):
        # Crea la consulta
        resultado = db.query(
                cast(
                    func.concat(
                        func.extract('year', DataSetEntrenamiento.fecha),
                        "-",
                        func.extract('month', DataSetEntrenamiento.fecha),
                        "-1"
                    ), Date
                ).label("anio_mes"),
                func.sum(DataSetEntrenamiento.monto).label("monto")
            )\
            .where(
                DataSetEntrenamiento.usuario == usuario,
                DataSetEntrenamiento.categoria == categoria
            )\
            .group_by("anio_mes")\
            .order_by("anio_mes")\
            .all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos para mostrar"}
            )
        return resultado

#? CATEGORICO

    def consultar_prediccion_categorico(self, usuario, db: Session):
        resultado = db.query(
                DataSetEntrenado.categoria,
                func.sum(DataSetEntrenado.monto).label("monto")
            )\
            .where(
                DataSetEntrenado.usuario == usuario
            )\
            .group_by(DataSetEntrenado.categoria)\
            .order_by("categoria")\
            .all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos para mostrar"}
            )
        return resultado

    def consultar_historico_categorico(self, usuario, db: Session):
        resultado = db.query(
                DataSetEntrenamiento.categoria,
                func.sum(DataSetEntrenamiento.monto).label("monto")
            )\
            .where(
                DataSetEntrenamiento.usuario == usuario
            )\
            .group_by(DataSetEntrenamiento.categoria)\
            .order_by("categoria")\
            .all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos para mostrar"}
            )
        return resultado
    
    def consultar_categorico_mensual(self, categoria, mes, usuario, db : Session):
        # Subconsulta para dataset_entrenado
        stmt1 = select(
            DataSetEntrenado.anio,
            func.sum(DataSetEntrenado.monto).label("monto")
        ).where(
            (DataSetEntrenado.categoria == categoria) & 
            (DataSetEntrenado.mes == mes) &
            (DataSetEntrenado.usuario == usuario)
        ).group_by(
            DataSetEntrenado.anio, 
        )
        # Subconsulta para dataset_entrenamiento
        stmt2 = select(
            extract("year", DataSetEntrenamiento.fecha).label("anio"),
            func.sum(DataSetEntrenamiento.monto).label("monto")
        ).where(
            (DataSetEntrenamiento.categoria == categoria) & 
            (extract("month", DataSetEntrenamiento.fecha) == mes) &
            (DataSetEntrenamiento.usuario == usuario)
        ).group_by(
            extract("year", DataSetEntrenamiento.fecha),
        )
        # Unión de las dos consultas
        union_stmt = union_all(stmt1, stmt2).subquery()

        # Aplicar ORDER BY sobre la unión
        query = select(
            union_stmt.c.anio,
            union_stmt.c.monto
        ).order_by(union_stmt.c.anio,)

        # Ejecutar la consulta
        try:
            return db.execute(query).mappings().all()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ocurrion un error: {str(e)}") from e
