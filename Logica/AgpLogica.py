from datetime import timedelta
import os, time, shutil, io


from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

import pandas as pd

from Persistencia.PersistenciaFacade import AccesoDatosFacade

from Schemas.AnexoGatosPersonalesSchema import AgpDatosConsulta



class AgpLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()
        self.output_dir = os.path.abspath("AnexosGastosPersonales")  # carpeta de descarga

    def agp_datos_lista(self, identificacion_comprador, cod_periodo_fiscal, db : Session):
        comprador = self.facade.comprador_find_one(identificacion_comprador, db)
        if not comprador:
            return JSONResponse(
                status_code=200,
                content={"message": f"No se encontro el comprador con indentificación {identificacion_comprador}"}
            )
        periodo_fiscal = self.facade.periodo_fiscal_find_one(cod_periodo_fiscal, db)
        datos = AgpDatosConsulta(
            identificacion_comprador = identificacion_comprador,
            periodo_fiscal = periodo_fiscal.periodo_fiscal
        )
        return self.facade.agp_datos_lista(datos, db)

    def generar_agp(self, identificacion_comprador, cod_periodo_fiscal, db : Session):
        agp = self.agp_datos_lista(identificacion_comprador, cod_periodo_fiscal, db)
        # Datos para la tabla

        # Crear DataFrame
        df = pd.DataFrame(agp)
        # Renombrar las columnas
        df.rename(
            columns={
                "ruc_proveedor": "RUC PROVEEDOR",
                "cantidad_comprobantes": "CANTIDAD DE COMPROBANTES",
                "base_imponible": "BASE IMPONIBLE",
                "tipo_gasto": "TIPO DE GASTO",
            },
            inplace=True,
        )

        # Formatear la columna BASE_IMPONIBLE
        df["BASE IMPONIBLE"] = df["BASE IMPONIBLE"].apply(lambda x: f"$ {x:.2f}")

        # Guardar el Excel en memoria
        output = io.BytesIO()
        df.to_excel(output, index=False, sheet_name="Detalle Gastos con Proveedor")
        output.seek(0)  # Volver al inicio del archivo

        # Devolver el archivo como respuesta con StreamingResponse
        filename = "Anexo Gastos Personales.xlsx"
        headers = {"filename": filename}

        return StreamingResponse(
            output,  # Pasa el objeto BytesIO
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
