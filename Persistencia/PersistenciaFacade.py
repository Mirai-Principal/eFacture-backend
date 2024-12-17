from sqlalchemy.orm import Session
from Persistencia.Crud import UsuariosCrud
from Persistencia.Crud import MembresiasCrud


class AccesoDatosFacade:
    """Fachada para la capa de persistencia. Centraliza las operaciones."""

    def __init__(self):
        self.UsuariosCrud = UsuariosCrud.UsuariosCrud()  # Instancia de UsuariosCrud para este contexto
        self.MembresiasCrud = MembresiasCrud.MembresiasCrud()


    # Métodos relacionados con usuarios
    def create_user(self, datos, db : Session):
        return self.UsuariosCrud.create_user(datos, db)
    def get_user_by_email(self, correo: str, db : Session):
        return self.UsuariosCrud.get_user_by_email(correo, db)
    def get_user_by_identificacion(self, correo: str, db : Session):
        return self.UsuariosCrud.get_user_by_email(correo, db)
    
    def update_password(self, datos, db : Session):
        return self.UsuariosCrud.update_password(datos, db)

    def lista_membresias(self, db : Session):
        return self.MembresiasCrud.get_membresias(db)
    def nueva_membresia(self, datos, db : Session):
        return self.MembresiasCrud.nueva_membresia(datos, db)
    def actualizar_membresia(self, datos, db : Session):
        return self.MembresiasCrud.actualizar_membresia(datos, db)
    
    def visualizar_membresia(self, cod, db : Session):
        return self.MembresiasCrud.get_membresia_by_id(cod, db)