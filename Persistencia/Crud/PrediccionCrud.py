from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import cast, Date, text, select
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
        # Usar bulk_insert_mappings para insertar de manera eficiente
        try:
            db.bulk_insert_mappings(DataSetEntrenado, datos)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ocurrion un error: {str(e)}") from e