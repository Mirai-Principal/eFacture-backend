from datetime import datetime, date
from pydantic import BaseModel, Field


class FraccionBasicaCreate(BaseModel):
    cod_fraccion_basica : int = None
    cod_periodo_fiscal : int
    valor_fraccion_basica : float = Field(..., ge=0)

class FraccionBasicaList(FraccionBasicaCreate):
    created_at : date
    periodo_fiscal : float





class FraccionBasicaDelete(BaseModel):
    cod_fraccion_basica : int
  