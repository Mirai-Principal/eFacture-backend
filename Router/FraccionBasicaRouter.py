from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Logica.FraccionBasicaLogica import FraccionBasicaLogica
from Schemas.FraccionBasicaSchema import FraccionBasicaCreate, FraccionBasicaList, FraccionBasicaDelete

from Persistencia.Conexion import DataBase

router = APIRouter()
FraccionBasicaLogica = FraccionBasicaLogica()

@router.post('/fraccion_basica_insert')
def fraccion_basica_insert( datos : FraccionBasicaCreate, db : Session = Depends(DataBase.get_db)):
    return FraccionBasicaLogica.fraccion_basica_insert(datos, db)

@router.get('/fraccion_basica_list' , response_model=List[FraccionBasicaList])
def fraccion_basica_list(db : Session = Depends(DataBase.get_db)):
    return FraccionBasicaLogica.fraccion_basica_list(db)

@router.post('/fraccion_basica_delete' , response_model=List[FraccionBasicaList])
def fraccion_basica_delete(datos : FraccionBasicaDelete ,db : Session = Depends(DataBase.get_db)):
    return FraccionBasicaLogica.fraccion_basica_delete(datos, db)