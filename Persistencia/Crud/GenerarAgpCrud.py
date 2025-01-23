from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy import func, extract, and_
from sqlalchemy import cast, Date
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from Persistencia.Models.AnexoGatosPersonales import AnexoGatosPersonales as AGP
from Persistencia.Models.Usuarios import Usuarios 

# para generar los datos del AGP
from Persistencia.Models.Comprobantes import Comprobantes
from Persistencia.Models.Detalles import Detalles
from Persistencia.Models.Categorias import Categorias
from Persistencia.Models.Comprador import Comprador


from Persistencia.Models.PeriodoFiscal import PeriodoFiscal
from Schemas.AnexoGatosPersonalesSchema import (AgpCreate, AgpDatosConsulta, AgpDatosGenerarXml)

class GenerarAgpCrud:    
    def agp_datos_lista(self, datos : AgpDatosConsulta, db : Session):
        try:
            resultado = db.query(
                Comprobantes.ruc.label("ruc_proveedor"),
                func.sum(Detalles.detalle_valor).label("base_imponible"),
                func.count(Comprobantes.ruc).label("cantidad_comprobantes"),
                Categorias.categoria.label("tipo_gasto"),
            )\
            .join(Detalles, Detalles.cod_comprobante == Comprobantes.cod_comprobante)\
            .join(Categorias, Categorias.cod_categoria == Detalles.cod_categoria)\
            .join(Comprador, Comprador.cod_comprador == Comprobantes.cod_comprador)\
            .group_by(Comprobantes.ruc, Categorias.categoria)\
            .where(
                and_(
                    extract('year', Comprobantes.fecha_emision) == datos.periodo_fiscal,
                    Comprador.identificacion_comprador == datos.identificacion_comprador
                )
            )\
            .all()
            if not resultado:
                return JSONResponse(
                    status_code=200,
                    content={"message": "No hay datos registrados"}
                )
            return resultado
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=f"Ocurrio un error {str(e)}") from e

    def agp_datos_beneficiaria_pension(self, datos : AgpDatosGenerarXml, db : Session):
        try:
            resultado = db.query(
                func.sum(Detalles.detalle_valor).label("valor_pensiones"),
                Categorias.categoria.label("tipo_gasto"),
            )\
            .select_from(Comprobantes)\
            .join(Detalles, Detalles.cod_comprobante == Comprobantes.cod_comprobante)\
            .join(Categorias, Categorias.cod_categoria == Detalles.cod_categoria)\
            .join(Comprador, Comprador.cod_comprador == Comprobantes.cod_comprador)\
            .group_by(Categorias.categoria)\
            .where(
                and_(
                    extract('year', Comprobantes.fecha_emision) == datos.periodo_fiscal,
                    Comprador.identificacion_comprador == datos.beneficiariaPension
                )
            )\
            .all()
            if not resultado:
                return JSONResponse(
                    status_code=200,
                    content={"message": "No hay datos registrados"}
                )
            return resultado
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=f"Ocurrio un error {str(e)}") from e


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
            raise HTTPException(status_code=400, detail=f"Ya existe un {tabla} con los mismo datos") from e
        except DataError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error de datos: tipos o formato incorrecto") from e
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error interno: datos con formato incorrecto {str(e)}") from e
        return consulta