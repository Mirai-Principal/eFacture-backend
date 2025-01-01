from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from Logica.UsuarioMembresiaLogica import UsuarioMembresiaLogica


from Schemas.UsuarioMembresiaSchema import UsuarioMembresia

from Persistencia.Conexion import DataBase

router = APIRouter()

UsuarioMembresiaLogica = UsuarioMembresiaLogica()

@router.get('/mi_suscripcion', response_model = UsuarioMembresia)
def visualizar_mi_suscripcion( db : Session = Depends(DataBase.get_db)):
    return UsuarioMembresiaLogica.visualizar_mi_suscripcion(db)