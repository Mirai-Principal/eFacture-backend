from fastapi import APIRouter, Depends, Request
from typing import List
from sqlalchemy.orm import Session
from Logica.UsuarioMembresiaLogica import UsuarioMembresiaLogica


from Schemas.UsuarioMembresiaSchema import UsuarioMembresia, EstadoSuscripcion

from Persistencia.Conexion import DataBase

router = APIRouter()

UsuarioMembresiaLogica = UsuarioMembresiaLogica()

@router.get('/mi_suscripcion', response_model = UsuarioMembresia)
def visualizar_mi_suscripcion(request : Request, db : Session = Depends(DataBase.get_db)):
    return UsuarioMembresiaLogica.visualizar_mi_suscripcion(request, db)


@router.get('/mi_suscripcion/estado', response_model = EstadoSuscripcion)
def get_estado_suscripcion(request : Request, db : Session = Depends(DataBase.get_db)):
    return UsuarioMembresiaLogica.get_estado_suscripcion(request, db)