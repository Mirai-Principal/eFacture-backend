from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import extract
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from Persistencia.Models.Comprobantes import Comprobantes
from Persistencia.Models.Comprador import Comprador
from Persistencia.Models.Detalles import Detalles
from Schemas.ComprobantesSchema import (CompradorCreate, ComprobantesCreate, DetallesCreate, ComprobantesLista, DetallesUpdate)

class ComprobantesCrud:
# Comprador
    def comprador_insert(self, datos: CompradorCreate, db : Session):
        consulta = Comprador(
            identificacion_comprador = datos.identificacion_comprador,
            razon_social_comprador = datos.razon_social_comprador,
        )
        db.add(consulta)  # Agregar el objeto actualizado al contexto de la sesión
        db.commit()
        db.refresh(consulta)
        return consulta

    def comprador_find_one(self, identificacion_comprador, db : Session):
        return db.query(Comprador).where(Comprador.identificacion_comprador == identificacion_comprador).first()
    def lista_compradores(self, db : Session):
        resultado = db.query(Comprador).all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        return resultado

# Comprobantes
    def comprobante_find_one(self, clave_acceso, db : Session):
        return db.query(Comprobantes).where(Comprobantes.clave_acceso == clave_acceso).first()

    def comprobante_insert(self, datos : ComprobantesCreate, db : Session):
        consulta = Comprobantes(
            cod_comprador = datos.cod_comprador,
            archivo = datos.archivo,
            clave_acceso = datos.clave_acceso,
            razon_social = datos.razon_social,
            fecha_emision = datos.fecha_emision,
            importe_total = datos.importe_total
        )
        db.add(consulta)  # Agregar el objeto actualizado al contexto de la sesión
        db.commit()
        db.refresh(consulta)
        return consulta
    def lista_comprobantes(self, datos : ComprobantesLista, db : Session):
         # Inicia la consulta base
        consulta = db.query(Comprobantes).where(Comprobantes.cod_comprador == datos.cod_comprador)

        # Agrega condiciones dinámicamente
        if datos.anio:
            consulta = consulta.where(extract('year', Comprobantes.fecha_emision) == datos.anio)
        if datos.mes:
            consulta = consulta.where(extract('month', Comprobantes.fecha_emision) == datos.mes)
        if datos.dia != "Todos":
            consulta = consulta.where(extract('day', Comprobantes.fecha_emision) == datos.dia)
        
         # Ejecuta la consulta
        resultado = consulta.all()
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados para esta fecha"}
            )
        return resultado
    
    
# detalles
    def detalle_insert(self, datos : DetallesCreate, db : Session):
        consulta = Detalles(
            cod_categoria = datos.cod_categoria,
            cod_comprobante = datos.cod_comprobante,
            descripcion = datos.descripcion,
            cantidad = datos.cantidad,
            precio_unitario = datos.precio_unitario,
            precio_total_sin_impuesto = datos.precio_total_sin_impuesto,
            impuesto_valor = datos.impuesto_valor,
            detalle_valor = datos.detalle_valor
        )
        db.add(consulta)
        db.commit()
        db.refresh(consulta)
        return consulta
    
    def detalles_comprobante(self, cod_comprobante, db : Session):
        return db.query(Detalles).where(Detalles.cod_comprobante == cod_comprobante).all()
    def detalles_update(self, datos : DetallesUpdate, db : Session):
        resultado = db.query(Detalles).where(Detalles.cod_detalle == datos.cod_detalle).first()
        resultado.cod_categoria = datos.cod_categoria
         # Confirmar los cambios en la base de datos
        db.add(resultado)  # Agregar el objeto actualizado al contexto de la sesión
        db.commit()
        db.refresh(resultado)
        return JSONResponse(
            status_code=200,
            content={"message": "Se han guardado los datos"}
        )
