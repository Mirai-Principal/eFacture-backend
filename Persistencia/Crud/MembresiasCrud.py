from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError

from fastapi import HTTPException
from fastapi.responses import JSONResponse


from Persistencia.Models import (Membresias, UsuarioMembresia)

from Schemas import (MembresiaSchema)

class MembresiasCrud:
    def get_membresias(self, db : Session):
        return db.query(Membresias.Membresias).all()

    def lista_memb_disponibles(self, db : Session):
        return db.query(Membresias.Membresias).where(Membresias.Membresias.estado == "disponible").order_by(Membresias.Membresias.precio).all()

    def nueva_membresia(self, datos : MembresiaSchema.Membresia, db : Session):
        query = Membresias.Membresias(
            nombre_membresia = datos.nombre_membresia,
            descripcion_membresia = datos.descripcion_membresia,
            caracteristicas = datos.caracteristicas,
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
        resultado.caracteristicas = datos.caracteristicas
        resultado.precio = datos.precio
        resultado.cant_comprobantes_carga = datos.cant_comprobantes_carga
        resultado.estado = datos.estado
        resultado.fecha_lanzamiento = datos.fecha_lanzamiento
        resultado.vigencia_meses = datos.vigencia_meses
        resultado.fecha_finalizacion = datos.fecha_finalizacion
        return self.get_exception(resultado, db)
    
    def generar_suscripcion(self, datos : MembresiaSchema.PagoMembresia, db : Session):
        consulta = UsuarioMembresia.UsuarioMembresia(
            cod_usuario = datos.cod_usuario,
            cod_membresia = datos.cod_membresia,
            order_id_paypal = datos.orderID,
            estado_membresia = datos.estado_membresia,
            cant_comprobantes_permitidos = datos.cant_comprobantes_permitidos,
        )
        try:
            # Confirmar los cambios en la base de datos
            db.add(consulta)  # Agregar el objeto actualizado al contexto de la sesión
            db.commit()
            db.refresh(consulta)
            return HTTPException(status_code=200, detail="Se han guardado los datos")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error interno: No se han guardado los datos {str(e)}") from e

    
    def get_exception(self, consulta, db : Session):
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
            raise HTTPException(status_code=400, detail="Ya existe una membresia con el mismo nombre") from e
        except DataError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error de datos: tipos o formato incorrecto") from e
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error interno: datos con formato incorrecto {e}") from e
        return consulta