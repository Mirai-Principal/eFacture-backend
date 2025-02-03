from datetime import datetime, timedelta

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jose import JWTError, jwt, ExpiredSignatureError


import pytz

from Configuracion import Config

# Definir la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

class OptionsToken:
    @staticmethod
    def create_access_token(data: dict, tiempo_expiracion_minutos: int ):
        to_encode = data.copy()
        expire = datetime.now(ecuador_tz) + timedelta(minutes=tiempo_expiracion_minutos)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Config.PRIVATE_KEY, algorithm="RS256")
        return encoded_jwt
    
    @staticmethod
    def get_info_token(token):
        # Decodificar el token
        try:
            payload = jwt.decode(token, Config.PUBLIC_KEY, algorithms=["RS256"])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
            return payload
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Token inválido") from e

# Middleware personalizado
class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # pasar por alto para q el CORS devuelva la respuesta al navegador
        if request.method == "OPTIONS":
            # print(request.headers.get("Authorization"))
            return await call_next(request)

        #!solo para DESARROLLO para evaluar la API
        if request.url.path in ["/docs", "/openapi.json", "/redoc"] and Config.ENTORNO == "development":
            return await call_next(request)

        #? Permitir acceso a la ruta de login sin token
        if request.url.path in ["/login", "/", "/password_reset", "/registrar"]:
            return await call_next(request)

        token = request.headers.get("Authorization")
        # Token no proporcionado
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No permitido")
        
        # Extraer el token (formato esperado: "Bearer <token>")
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Formato de token inválido")

        try:
            # Decodificar el token
            payload = jwt.decode(token, Config.PUBLIC_KEY, algorithms=["RS256"])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
            
            exp = payload.get("exp")
            # verifica q no haya expirado el link y solo lo renova si no es cambiar_password
            if exp and datetime.utcfromtimestamp(exp) - datetime.utcnow() < timedelta(minutes=1) and request.url.path != "/cambiar_password":
                # reinicia el tiempo del token
                token = OptionsToken.create_access_token(payload, 30)

            # Continuar con la solicitud y devolver el nuevo token en la respuesta
            response = await call_next(request)
            response.headers["Authorization"] = f"Bearer {token}"
            response.headers["sub"] = user_id
            response.headers["tipo_usuario"] = payload.get("tipo_usuario")

            # response.headers["exp"] = str(exp)
            return response

        except ExpiredSignatureError as e:
            # Manejo de error por token expirado
            if request.url.path == "/cambiar_password":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Link expirado, vuelva solicitar cambiar la contraseña") from e
            else:
                return JSONResponse( status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "La sesión ha expirado"}, )
        except JWTError as e:
            # Manejo de error general de JWT
            return JSONResponse( status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Token no válido o expirado"}, )
