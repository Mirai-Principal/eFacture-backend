from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import and_, cast, Date, select

from fastapi import HTTPException
from fastapi.responses import JSONResponse

import pytz
# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

from Persistencia.Models.Membresias import Membresias
from Persistencia.Models.UsuarioMembresia import UsuarioMembresia

from Schemas.UsuarioMembresiaSchema import MiSuscripcion

class UsuarioMembresiaCrud:
    def visualizar_mi_suscripcion(self,cod_usuario : int, db : Session):
        try:
            stmt = (
                select(
                    UsuarioMembresia.cod_usuario,
                    UsuarioMembresia.cod_membresia,
                    Membresias.nombre_membresia,
                    Membresias.descripcion_membresia,
                    Membresias.caracteristicas,
                    Membresias.cant_comprobantes_carga,
                    UsuarioMembresia.estado_membresia,
                    UsuarioMembresia.cant_comprobantes_permitidos,
                    cast(UsuarioMembresia.created_at.label("fecha_compra"), Date),
                    cast(UsuarioMembresia.fecha_vencimiento, Date),
                    UsuarioMembresia.order_id_paypal,
                )
                .join(
                    UsuarioMembresia,
                    Membresias.cod_membresia == UsuarioMembresia.cod_membresia,
                )
                .where(and_(
                    UsuarioMembresia.estado_membresia == "vigente",
                    UsuarioMembresia.cod_usuario == cod_usuario
                ))
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
    
    def descontar_cant_comprobantes(self, cod_usuario, db : Session):
        suscripcion = db.query(UsuarioMembresia).where(
            and_(
                    UsuarioMembresia.cod_usuario == cod_usuario,
                    UsuarioMembresia.estado_membresia == "vigente",
                )
        ).first()

        suscripcion.cant_comprobantes_permitidos -= 1
        db.add(suscripcion)  # Agregar el objeto actualizado al contexto de la sesión
        db.commit()
        db.refresh(suscripcion)
        
        if(suscripcion.cant_comprobantes_permitidos == 0):
            self.update_estado_suscripcion(suscripcion.order_id_paypal, db)
            raise HTTPException(status_code=500,detail="Llegaste al limite de carga de comprobates en tu suscripción") from e

        return suscripcion
        
    def get_estado_suscripcion(self, cod_usuario, db : Session):
        suscripcion = db.query(UsuarioMembresia).where(
            and_(
                    UsuarioMembresia.cod_usuario == cod_usuario,
                    UsuarioMembresia.estado_membresia == "vigente",
                )
        ).first()
        if not suscripcion:
                return JSONResponse(
                    status_code=200,
                    content={"message": "No tienes una suscripción vigente"}
                )
        return suscripcion