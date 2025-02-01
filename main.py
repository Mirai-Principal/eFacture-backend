from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

from Middlewares import JWTMiddleware

# from Persistencia.Models import Usuarios
from Router import (
    UsuariosRouter, MembresiasRouter, UsuarioMembresiaRouter, 
    CategoriasRouter, ComprobantesRouter, PeriodoFiscalRouter, 
    FraccionBasicaRouter, AgpRouter, PrediccionRouter, ConfiguracionRouter
    )

app = FastAPI()

origins = [
    "http://localhost:5173",  # Adjust the port if your frontend runs on a different one
    "https://yourfrontenddomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins from the list - acceso desde el frontend
    allow_credentials=True, # para uso de tokens y cookies / información de credenciales en los encabezados
    allow_methods=["GET", "POST", "DELETE", "PUT"],  # Allows methods que el frontend puede solicitar
    allow_headers=["*"],  # Allows all headers que vienen desde el frontend
    expose_headers=["Authorization", "sub", "tipo_usuario", "filename"],  # Permite que el frontend vea los encabezados
    max_age=3600,  # Cachea la respuesta preflight por 1 hora
)


# Iniciar la base de datos
# Usuarios.Base.metadata.create_all(bind=DataBase.engine)

# Agregar el middleware a la aplicación
app.add_middleware(JWTMiddleware.JWTMiddleware)

# Manejador de excepciones global
# Personalizar la excepción RequestValidationError cuando no cumple con el esquema de datos
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Los datos enviados no son válidos. Por favor, verifica el formato y vuelve a intentarlo.",
            "errors": exc.errors(),
            "body": exc.body if hasattr(exc, "body") else None
        },
    )


# agregar los routers
app.include_router(UsuariosRouter.router, tags=["usuarios"])
app.include_router(MembresiasRouter.router, tags=["membresias"])
app.include_router(UsuarioMembresiaRouter.router, tags=["membresias"])
app.include_router(CategoriasRouter.router, tags=["Categorias de comprobantes"])
app.include_router(ComprobantesRouter.router, tags=["Comprobantes"])
app.include_router(PeriodoFiscalRouter.router, tags=["Periodo Fiscal"])
app.include_router(FraccionBasicaRouter.router, tags=["Fraccion Basica"])
app.include_router(AgpRouter.router, tags=["Anexo de gatos personales"])

app.include_router(PrediccionRouter.router, tags=["Generacion y prediccion de datos"])
app.include_router(ConfiguracionRouter.router, tags=["Configuracion de la aplicacion"])

