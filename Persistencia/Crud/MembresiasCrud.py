from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from fastapi import HTTPException

from Persistencia.Models import Membresias
from Persistencia.Schemas import MembresiaSchema


class MembresiasCrud:
    def get_membresias(self, db : Session):
        return db.query(Membresias.Membresias).all()
    def nueva_membresia(self, datos : MembresiaSchema.Membresia, db : Session):
        query = Membresias.Membresias(
            nombre_membresia = datos.nombre_membresia,
            descripcion_membresia = datos.descripcion_membresia,
            precio = datos.precio,
            cant_comprobantes_carga = datos.cant_comprobantes_carga,
            estado = datos.estado,
            fecha_lanzamiento = datos.fecha_lanzamiento,
            vigencia_meses = datos.vigencia_meses,
            fecha_finalizacion = datos.fecha_finalizacion
        )

        try:
            db.add(query)
            db.commit()
            db.refresh(query)
        except DataError:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error de datos: tipos o formato incorrecto")
        except Exception:
            db.rollback()
            # raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error interno: datos con formato incorrecto")
        return query

    def get_membresia_by_id(self, cod : str, db : Session):
        return db.query(Membresias.Membresias).filter(Membresias.Membresias.cod_membresia == cod).first()
    
    def actualizar_membresia(self, datos : MembresiaSchema.MembresiaUpdate, db : Session):
        resultado = self.get_membresia_by_id(datos.cod_membresia, db)

        resultado.nombre_membresia = datos.nombre_membresia
        resultado.descripcion_membresia = datos.descripcion_membresia
        resultado.precio = datos.precio
        resultado.cant_comprobantes_carga = datos.cant_comprobantes_carga
        resultado.estado = datos.estado
        resultado.fecha_lanzamiento = datos.fecha_lanzamiento
        resultado.vigencia_meses = datos.vigencia_meses
        resultado.fecha_finalizacion = datos.fecha_finalizacion

        db.commit()
        db.refresh(resultado)
        return resultado