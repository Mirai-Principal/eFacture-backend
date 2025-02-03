from datetime import timedelta
import operator


from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Logica.Decoradores import Singleton

from Persistencia.PersistenciaFacade import AccesoDatosFacade

@Singleton
class ConfiguracionLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()

    def getOperador(self, operador):
        # Diccionario que mapea operadores a funciones
        OPERATORS = {
            '=': operator.eq,
            '==': operator.eq,
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '!=': operator.ne,
            'in': lambda x, y: x in y,  # Soporte para "in"
            'between': lambda x, y: y[0] <= x <= y[1],  # Soporte para rangos
        }
        return OPERATORS.get(operador)
    
    def configuracion_get_by_id(self, cod_regla : int, db : Session):
        return self.facade.ConfiguracionCrud.configuracion_get_by_id(cod_regla, db) 
    
    def configuracion_lista(self, db : Session):
        return self.facade.ConfiguracionCrud.configuracion_lista(db)

    def configuracion_get_by_nombre(self, nombre : str, db : Session):
        return self.facade.ConfiguracionCrud.configuracion_get_by_nombre(nombre, db)

    def configuracion_update(self, datos, db : Session):
        return self.facade.ConfiguracionCrud.configuracion_update(datos, db)
