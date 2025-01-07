from fastapi import APIRouter, Depends, Response, Request, HTTPException
import requests 

from typing import List
from sqlalchemy.orm import Session

from Persistencia.Conexion import DataBase

from bs4 import BeautifulSoup

router = APIRouter()

@router.get("/portal_sri")
def proxy(request: Request):
    # URL del SRI que deseas scrapeear
    url = "https://srienlinea.sri.gob.ec/auth/realms/Internet/protocol/openid-connect/auth?client_id=app-sri-claves-angular&redirect_uri=https%3A%2F%2Fsrienlinea.sri.gob.ec%2Fsri-en-linea%2F%2Fcontribuyente%2Fperfil&state=b709b8bc-9006-4265-ace1-be8664cd6ecc&nonce=d22fb123-149c-4a22-8a79-e063a4fb18ce&response_mode=fragment&response_type=code&scope=openid"

    # Encabezados para simular un navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        # Hacer la solicitud HTTP
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica si hubo un error en la solicitud

        # Parsear el contenido HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # Extraer datos específicos
        # print(soup.prettify())  # Muestra el contenido HTML formateado
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer scraping: {e}")
