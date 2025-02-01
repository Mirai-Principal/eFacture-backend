from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from Logica.ConfiguracionLogica import ConfiguracionLogica
from Schemas.ConfiguracionSchema import ConfiguracionUpdate, ConfiguracionLista

from Persistencia.Conexion import DataBase

router = APIRouter()
ConfiguracionLogica = ConfiguracionLogica()

@router.get('/configuracion/{cod_regla}', response_model=ConfiguracionUpdate)
def configuracion_get_by_id(cod_regla : int, db : Session = Depends(DataBase.get_db)):
    return ConfiguracionLogica.configuracion_get_by_id(cod_regla, db)

@router.get('/configuracion_lista', response_model=List[ConfiguracionLista])
def configuracion_lista(db : Session = Depends(DataBase.get_db)):
    return ConfiguracionLogica.configuracion_lista(db)


@router.put('/configuracion')
def configuracion_update(datos : ConfiguracionUpdate, db : Session = Depends(DataBase.get_db)):
    return ConfiguracionLogica.configuracion_update(datos, db)