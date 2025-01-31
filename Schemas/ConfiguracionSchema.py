from datetime import datetime, date
from pydantic import BaseModel, Field

class ConfiguracionUpdate(BaseModel):
    cod_regla : int
    nombre : str
    descripcion : str
    campo : str
    operador : str
    valor : str 

class ConfiguracionLista(ConfiguracionUpdate):
    created_at : datetime
    updated_at : datetime