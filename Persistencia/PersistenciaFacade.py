from sqlalchemy.orm import Session
from Persistencia.Crud import (UsuariosCrud, MembresiasCrud, UsuarioMembresiaCrud, PeriodoFiscalCrud , CategoriasCrud, ComprobantesCrud)


class AccesoDatosFacade:
    """Fachada para la capa de persistencia. Centraliza las operaciones."""

    def __init__(self):
        self.UsuariosCrud = UsuariosCrud.UsuariosCrud()  # Instancia de UsuariosCrud para este contexto
        self.MembresiasCrud = MembresiasCrud.MembresiasCrud()
        self.UsuarioMembresiaCrud = UsuarioMembresiaCrud.UsuarioMembresiaCrud()
        self.PeriodoFiscalCrud = PeriodoFiscalCrud.PeriodoFiscalCrud()
        self.CategoriasCrud = CategoriasCrud.CategoriasCrud()
        self.ComprobantesCrud = ComprobantesCrud.ComprobantesCrud()


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

# periodo fiscal
    def periodo_fiscal_insert(self, datos, db : Session):
        return self.PeriodoFiscalCrud.periodo_fiscal_insert(datos, db)
    def periodo_fiscal_lista(self, db : Session):
        return self.PeriodoFiscalCrud.periodo_fiscal_lista(db)
    def periodo_fiscal_delete(self, datos, db : Session):
        return self.PeriodoFiscalCrud.periodo_fiscal_delete(datos, db)

    # categorias
    def categoria_insert(self, datos, db : Session):
        return self.CategoriasCrud.categoria_insert(datos, db)
    def categorias_lista(self, db : Session):
        return self.CategoriasCrud.categorias_lista(db)
    def categoria_update(self, datos, db : Session):
        return self.CategoriasCrud.categoria_update(datos, db)

    # comprador
    def comprador_insert(self, datos, db : Session):
        return self.ComprobantesCrud.comprador_insert(datos, db)
    def comprador_find_one(self, identificacion_comprador, db : Session):
        return self.ComprobantesCrud.comprador_find_one(identificacion_comprador, db)
    def lista_compradores(self, db : Session):
        return self.ComprobantesCrud.lista_compradores(db)

    # comprobantes
    def comprobante_find_one(self, clave_acceso, db : Session):
        return self.ComprobantesCrud.comprobante_find_one(clave_acceso, db)

    def comprobante_insert(self, datos, db : Session):
        return self.ComprobantesCrud.comprobante_insert(datos, db)
    def lista_comprobantes(self, datos, db : Session):
        return self.ComprobantesCrud.lista_comprobantes(datos, db)

    # detalles comprobante
    def detalle_insert(self, datos, db : Session):
        return self.ComprobantesCrud.detalle_insert(datos, db)
    def detalles_comprobante(self, cod_comprobante, db : Session):
        return self.ComprobantesCrud.detalles_comprobante(cod_comprobante, db)
    def detalles_update(self, datos, db : Session):
        repr = self.ComprobantesCrud.detalles_update(datos, db)
