from datetime import datetime, date
from pydantic import BaseModel, Field

class AgpCreate(BaseModel):
    cod_usuario : int
    cod_periodo_fiscal : int
    valor_total_agp : float
    archivo_agp : str

class AgpLista(AgpCreate):
    cod_agp : int
    created_at : date
    periodo_fiscal : int

class AgpDatosConsulta(BaseModel):
    identificacion_comprador : str
    periodo_fiscal : int

class AgpDatos(BaseModel):
    ruc_proveedor: str
    base_imponible : float
    cantidad_comprobantes : int
    tipo_gasto : str