from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from Logica.ConfiguracionLogica import ConfiguracionLogica
from Schemas.ConfiguracionSchema import ConfiguracionUpdate, ConfiguracionLista

from Persistencia.Conexion import DataBase

router = APIRouter()
ConfiguracionLogica = ConfiguracionLogica()

@router.get('/configuracion_lista', response_model=List[ConfiguracionLista])
def configuracion_lista(db : Session = Depends(DataBase.get_db)):
    return ConfiguracionLogica.configuracion_lista(db)