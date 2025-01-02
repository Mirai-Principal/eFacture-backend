from sqlalchemy.orm import Session
from Persistencia.Crud import (UsuariosCrud, MembresiasCrud, UsuarioMembresiaCrud, SueldoBasicoCrud , CategoriasCrud)


class AccesoDatosFacade:
    """Fachada para la capa de persistencia. Centraliza las operaciones."""

    def __init__(self):
        self.UsuariosCrud = UsuariosCrud.UsuariosCrud()  # Instancia de UsuariosCrud para este contexto
        self.MembresiasCrud = MembresiasCrud.MembresiasCrud()
        self.UsuarioMembresiaCrud = UsuarioMembresiaCrud.UsuarioMembresiaCrud()
        self.SueldoBasicoCrud = SueldoBasicoCrud.SueldoBasicoCrud()
        self.CategoriasCrud = CategoriasCrud.CategoriasCrud()


# Métodos relacionados con usuarios
    def create_user(self, datos, db : Session):
        return self.UsuariosCrud.create_user(datos, db)
    def get_user_by_email(self, correo: str, db : Session):
        return self.UsuariosCrud.get_user_by_email(correo, db)
    def get_user_by_identificacion(self, correo: str, db : Session):
        return self.UsuariosCrud.get_user_by_email(correo, db)
    
    def update_password(self, datos, db : Session):
        return self.UsuariosCrud.update_password(datos, db)

# membresias
    def lista_membresias(self, db : Session):
        return self.MembresiasCrud.get_membresias(db)
    def lista_memb_disponibles(self, db : Session):
        return self.MembresiasCrud.lista_memb_disponibles(db)
    def nueva_membresia(self, datos, db : Session):
        return self.MembresiasCrud.nueva_membresia(datos, db)
    def actualizar_membresia(self, datos, db : Session):
        return self.MembresiasCrud.actualizar_membresia(datos, db)
    
    def visualizar_membresia(self, cod, db : Session):
        return self.MembresiasCrud.get_membresia_by_id(cod, db)
# suscripcion
    def generar_suscripcion(self, datos, db : Session):
        return self.MembresiasCrud.generar_suscripcion(datos, db)
    def visualizar_mi_suscripcion(self, db : Session):
        return self.UsuarioMembresiaCrud.visualizar_mi_suscripcion(db)

# sueldo basico
    def sueldo_basico_insert(self, datos, db : Session):
        return self.SueldoBasicoCrud.sueldo_basico_insert(datos, db)
    def lista_sueldo_basico(self, db : Session):
        return self.SueldoBasicoCrud.lista_sueldo_basico(db)

    # categorias
    def categoria_insert(self, datos, db : Session):
        return self.CategoriasCrud.categoria_insert(datos, db)
    def categorias_lista(self, db : Session):
        return self.CategoriasCrud.categorias_lista(db)
    def categoria_update(self, datos, db : Session):
        return self.CategoriasCrud.categoria_update(datos, db)
