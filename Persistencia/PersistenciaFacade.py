from sqlalchemy.orm import Session
from .Crud import UsuariosCrud

class AccesoDatosFacade:
    """Fachada para la capa de persistencia. Centraliza las operaciones."""

    def __init__(self):
        self.UsuariosCrud = UsuariosCrud.UsuariosCrud()  # Instancia de UsuariosCrud para este contexto


    # Métodos relacionados con usuarios
    def create_user(self, datos, db : Session):
        return self.UsuariosCrud.create_user(datos, db)

    def get_user_by_email(self, correo: str, db : Session):
        return self.UsuariosCrud.get_user_by_email(correo, db)
    def get_user_by_identificacion(self, correo: str, db : Session):
        return self.UsuariosCrud.get_user_by_email(correo, db)
    
