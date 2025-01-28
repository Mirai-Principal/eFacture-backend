from datetime import datetime, date
from pydantic import BaseModel, Field

class CategoriaCreate(BaseModel):
    cod_categoria : int = None
    cod_fraccion_basica : int
    categoria : str = Field(..., max_length=50)
    descripcion_categoria : str
    cant_fraccion_basica : float

class CategoriaLista(CategoriaCreate):
    created_at : date
    valor_fraccion_basica : int
    periodo_fiscal: int

class CategoriasUnicas(BaseModel):
    categoria : str

  