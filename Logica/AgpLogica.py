from datetime import timedelta
import os, time, shutil, io


from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

import pandas as pd

from Persistencia.PersistenciaFacade import AccesoDatosFacade

from Schemas.AnexoGatosPersonalesSchema import AgpDatosConsulta, AgpDatosGenerarXml



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

    def generar_agp(self, datos : AgpDatosGenerarXml, db : Session):
        agp = self.agp_datos_lista(datos.identificacion_comprador, datos.cod_periodo_fiscal, db)
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

         # Reordenar las columnas
        column_order = [
            "RUC PROVEEDOR",
            "CANTIDAD DE COMPROBANTES",
            "BASE IMPONIBLE",
            "TIPO DE GASTO",
        ]
        df = df[column_order]

        # Formatear la columna BASE_IMPONIBLE
        # df["BASE IMPONIBLE"] = df["BASE IMPONIBLE"].apply(lambda x: f"$ {x:.2f}")

        #para las pensiones de alimentos
        if datos.beneficiariaPension:
            # formar dataframe a partir de los datos
            periodo_fiscal = self.facade.periodo_fiscal_find_one(datos.cod_periodo_fiscal, db)
            datos.periodo_fiscal = periodo_fiscal.periodo_fiscal
            
            datosBeneficiariaPension = self.facade.agp_datos_beneficiaria_pension(datos, db)
            df2 = pd.DataFrame(datosBeneficiariaPension)
            df2.rename(
                columns={
                    "valor_pensiones": "MONTO PENSIONES ALIMENTICIAS",
                    "tipo_gasto": "TIPO DE GASTO",
                },
                inplace=True,
            )

            df2["TIPO ID BENEFICIARIO PENSIÓN ALIMENTICIA"] = "CEDULA"
            df2["NÚMERO ID BENEFICIARIO PENSIÓN ALIMENTICIA"] = datos.beneficiariaPension


            # Reordenar las columnas para que la nueva columna sea la primera
            column_order = [
                "TIPO ID BENEFICIARIO PENSIÓN ALIMENTICIA",
                "NÚMERO ID BENEFICIARIO PENSIÓN ALIMENTICIA",
                "MONTO PENSIONES ALIMENTICIAS",
                "TIPO DE GASTO",
            ]
            df2 = df2[column_order]
        else:
            datosBeneficiariaPension = {
            "TIPO ID BENEFICIARIO PENSIÓN ALIMENTICIA": [],
            "NÚMERO ID BENEFICIARIO PENSIÓN ALIMENTICIA": [],
            "MONTO PENSIONES ALIMENTICIAS": [],
            "TIPO DE GASTO": [],
            }
            df2 = pd.DataFrame(datosBeneficiariaPension)

        

        #para GSP Valor No Cubierto Aseguradora
        if not datos.valorNoAsegurado:
            datos.valorNoAsegurado = 0
        datosValorNoAsegurado = {
        "VALORES NO CUBIERTOS POR ASEGURADORAS": [datos.valorNoAsegurado],
        }
        df3 = pd.DataFrame(datosValorNoAsegurado)


        # Guardar el Excel en memoria
        output = io.BytesIO()

        # Usar ExcelWriter para escribir múltiples hojas
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Detalle Gastos con Proveedor")
            df2.to_excel(writer, index=False, sheet_name="Detalle GSP Pensión Alimenticia")
            df3.to_excel(writer, index=False, sheet_name="GSP ValorNoCubiertoAseguradora")

        output.seek(0)  # Volver al inicio del archivo

        # Devolver el archivo como respuesta con StreamingResponse
        filename = "Anexo Gastos Personales.xlsx"
        headers = {"filename": filename}

        return StreamingResponse(
            output,  # Pasa el objeto BytesIO
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
