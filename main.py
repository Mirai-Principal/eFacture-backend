from fastapi import FastAPI
from Models import Usuarios
from Router import UsuariosRouter
from Conexion import DataBase
from fastapi.middleware.cors import CORSMiddleware

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
Usuarios.Base.metadata.create_all(bind=DataBase.engine)

app.include_router(UsuariosRouter.router)
