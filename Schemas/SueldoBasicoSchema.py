from datetime import datetime, date
from pydantic import BaseModel, Field

class SueldoBasicoCreate(BaseModel):
    cod_sueldo : int = None
    valor_sueldo: float = Field(..., gt=0)
    periodo_fiscal: date
    estado : str

    # created_at: datetime
    # updated_at: datetime
    # deleted_at: datetime = None
    # class Config:
    #     orm_mode = True
class SueldoBasicoLista(SueldoBasicoCreate):
    cod_sueldo : int
    created_at: datetime