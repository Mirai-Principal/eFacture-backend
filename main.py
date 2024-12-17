from fastapi import FastAPI
# from Persistencia.Conexion import DataBase
from fastapi.middleware.cors import CORSMiddleware

# from Persistencia.Models import Usuarios
from Router import UsuariosRouter, MembresiasRouter

app = FastAPI()

origins = [
    "http://localhost:5173",  # Adjust the port if your frontend runs on a different one
    "https://yourfrontenddomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins from the list - acceso desde el frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Iniciar la base de datos
# Usuarios.Base.metadata.create_all(bind=DataBase.engine)

app.include_router(UsuariosRouter.router)
app.include_router(MembresiasRouter.router)
