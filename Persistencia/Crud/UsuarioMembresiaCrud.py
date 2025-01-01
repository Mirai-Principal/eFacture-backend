from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy import cast, Date


import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')


from Persistencia.Models import (Membresias, UsuarioMembresia)


class UsuarioMembresiaCrud:
    def visualizar_mi_suscripcion(self, db : Session):
        try:
            stmt = (
                select(
                    UsuarioMembresia.UsuarioMembresia.cod_usuario,
                    UsuarioMembresia.UsuarioMembresia.cod_membresia,
                    Membresias.Membresias.nombre_membresia,
                    Membresias.Membresias.descripcion_membresia,
                    Membresias.Membresias.caracteristicas,
                    UsuarioMembresia.UsuarioMembresia.estado_membresia,
                    cast(UsuarioMembresia.UsuarioMembresia.created_at.label("fecha_compra"), Date),
                    cast(UsuarioMembresia.UsuarioMembresia.fecha_vencimiento, Date),
                    UsuarioMembresia.UsuarioMembresia.order_id_paypal,
                )
                .join(
                    UsuarioMembresia.UsuarioMembresia,
                    Membresias.Membresias.cod_membresia == UsuarioMembresia.UsuarioMembresia.cod_membresia,
                )
                .where(UsuarioMembresia.UsuarioMembresia.estado_membresia == "vigente")
            )

            # Ejecutar la consulta y obtener resultados como diccionarios
            resultado = db.execute(stmt).mappings().first()
            
            if not resultado:
                return JSONResponse(
                    status_code=200,
                    content={"message": "No tienes una suscripción vigente"}
                )
                
            # if(str(resultado.fecha_vencimiento) == "2026-01-01"):
            if(resultado.fecha_vencimiento <= datetime.now(ecuador_tz).date()):
                return self.update_estado_suscripcion(resultado.order_id_paypal, db)

            return resultado
        except Exception as e:
            raise HTTPException(status_code=500,detail=str(e)) from e
    def update_estado_suscripcion(self, order_id_paypal : str, db: Session):
        suscripcion = db.query(UsuarioMembresia.UsuarioMembresia).where(UsuarioMembresia.UsuarioMembresia.order_id_paypal == order_id_paypal).first()

        suscripcion.estado_membresia = suscripcion.estado_membresia = 'no vigente'
        db.add(suscripcion)  # Agregar el objeto actualizado al contexto de la sesión
        db.commit()
        db.refresh(suscripcion)
        return JSONResponse(
                status_code=200,
                content={"message": "Tu suscripción ha expirado"}
            )