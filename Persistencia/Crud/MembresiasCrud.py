from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from fastapi import HTTPException

from Persistencia.Models import Membresias
from Schemas import MembresiaSchema


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
        return self.get_exception(query, db)

    def get_membresia_by_id(self, cod : str, db : Session):
        resultado = db.query(Membresias.Membresias).filter(Membresias.Membresias.cod_membresia == cod).first()
        if not resultado:
            raise HTTPException(status_code=404, detail="Membresía no encontrada")
        return resultado
    
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
        return self.get_exception(resultado, db)
    
    def get_exception(self, consulta, db : Session):
        try:
            # Confirmar los cambios en la base de datos
            db.add(consulta)  # Agregar el objeto actualizado al contexto de la sesión
            db.commit()
            db.refresh(consulta)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Ya existe una membresia con el mismo nombre") from e
        except DataError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error de datos: tipos o formato incorrecto") from e
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error interno: datos con formato incorrecto") from e
        return consulta