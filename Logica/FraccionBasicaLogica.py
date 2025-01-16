from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Persistencia.PersistenciaFacade import AccesoDatosFacade

class FraccionBasicaLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()

    def fraccion_basica_insert(self, datos, db : Session):
        return self.facade.fraccion_basica_insert(datos, db)
    def fraccion_basica_list(self, db):
        return self.facade.fraccion_basica_list(db)
    def fraccion_basica_delete(self, datos, db):
        return self.facade.fraccion_basica_delete(datos, db)

    