from datetime import datetime, date
from pydantic import BaseModel, Field

class PeriodoFiscalCreate(BaseModel):
    cod_periodo_fiscal : int = None
    periodo_fiscal: int = Field(..., gt=2020)

class PeriodoFiscalLista(PeriodoFiscalCreate):
    created_at: datetime

class PeriodoFiscalDetele(BaseModel):
    cod_periodo_fiscal : int 