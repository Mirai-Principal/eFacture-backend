from fastapi import FastAPI
# from Persistencia.Conexion import DataBase
from fastapi.middleware.cors import CORSMiddleware

from Middlewares import JWTMiddleware

# from Persistencia.Models import Usuarios
from Router import (UsuariosRouter, MembresiasRouter, UsuarioMembresiaRouter, SueldoBasicoRouter, CategoriasRouter, ComprobantesRouter)

app = FastAPI()

origins = [
    "http://localhost:5173",  # Adjust the port if your frontend runs on a different one
    "https://yourfrontenddomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins from the list - acceso desde el frontend
    allow_credentials=True, # para uso de tokens y cookies / información de credenciales en los encabezados
    allow_methods=["GET", "POST"],  # Allows methods que el frontend puede solicitar
    allow_headers=["*"],  # Allows all headers que vienen desde el frontend
    expose_headers=["Authorization", "sub", "tipo_usuario"],  # Permite que el frontend vea los encabezados
    max_age=3600,  # Cachea la respuesta preflight por 1 hora
)


# Iniciar la base de datos
# Usuarios.Base.metadata.create_all(bind=DataBase.engine)

# Agregar el middleware a la aplicación
app.add_middleware(JWTMiddleware.JWTMiddleware)

# agregar los routers
app.include_router(UsuariosRouter.router, tags=["usuarios"])
app.include_router(MembresiasRouter.router, tags=["membresias"])
app.include_router(UsuarioMembresiaRouter.router, tags=["membresias"])
app.include_router(SueldoBasicoRouter.router, tags=["Suelo Basico"])
app.include_router(CategoriasRouter.router, tags=["Categorias de comprobantes"])
app.include_router(ComprobantesRouter.router, tags=["Comprobantes"])
