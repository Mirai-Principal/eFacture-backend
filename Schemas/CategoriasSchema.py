from datetime import datetime, date
from pydantic import BaseModel, Field

class CategoriaCreate(BaseModel):
    cod_categoria : int = None
    categoria : str = Field(..., max_length=50)
    descripcion_categoria : str
    cant_sueldos_basico : int 
class CategoriaLista(CategoriaCreate):
    created_at : datetime
    estado : str

class CategoriaUpdate(BaseModel):
    estado : str = Field(..., max_length=20)
  