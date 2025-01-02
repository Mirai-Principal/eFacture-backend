from datetime import datetime, date
from pydantic import BaseModel, Field

class SueldoBasicoCreate(BaseModel):
    valor_sueldo: float = Field(..., gt=0)
    periodo_fiscal: date
    # created_at: datetime
    # updated_at: datetime
    # deleted_at: datetime = None
    # class Config:
    #     orm_mode = True
class SueldoBasicoLista(SueldoBasicoCreate):
    cod_sueldo : str
    created_at: datetime