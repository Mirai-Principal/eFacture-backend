import os, time, shutil
from datetime import timedelta, datetime
import xml.etree.ElementTree as ET

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    WebDriverException
)

from Persistencia.PersistenciaFacade import AccesoDatosFacade
from Schemas.ComprobantesSchema import ParametrosExtraccion, CompradorCreate, ComprobantesCreate, DetallesCreate, ComprobantesLista

from Middlewares.JWTMiddleware import OptionsToken

class ComprobantesLogica:
    def __init__(self):
        self.facade = AccesoDatosFacade()
        self.key = "6Lc6rokUAAAAAJBG2M1ZM1LIgJ85DwbSNNjYoLDk"
        self.url = "https://srienlinea.sri.gob.ec/auth/realms/Internet/protocol/openid-connect/auth?client_id=app-sri-claves-angular&redirect_uri=https%3A%2F%2Fsrienlinea.sri.gob.ec%2Fsri-en-linea%2F%2Fcontribuyente%2Fperfil&state=eb4c53ac-d29d-401e-9d6f-610129870579&nonce=061ef4be-dc1e-4b1b-b02e-700ded45b915&response_mode=fragment&response_type=code&scope=openid"
        self.output_dir = os.path.abspath("comprobantes")  # carpeta de descarga
        self.cod_comprador = None
        self.cod_comprobante = None
        
    def RunProfile(self):
        # chrome://version/
        chrome_options = Options()
        chrome_options.add_argument(f'--load-extension={os.path.abspath("CaptchaSolver")}')
    

        prefs = {
            "download.default_directory": self.output_dir,  # Directorio donde se guardarán los archivos
            "download.prompt_for_download": False,  # No preguntar por descargas
            "download.directory_upgrade": True,  # Permitir actualizaciones en la carpeta de descargas
            "safebrowsing.enabled": True,  # Deshabilitar bloqueo de archivos no verificados
            "directory_upgrade": True    # Permitir la sobreescritura de archivos sin preguntar
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Configuración del driver en modo headless
        #? habilitar lo q de aqui cuando entre a produccion
        # chrome_options.add_argument("--headless")  # Ejecutar en modo headless
        chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU (opcional)
        # chrome_options.add_argument("--no-sandbox")  # Recomendado para entornos de servidor
        # chrome_options.add_argument("--disable-dev-shm-usage")  # Optimización para contenedores

        #! Si Selenium sigue teniendo problemas con páginas complejas en modo headless, considera migrar a herramientas como Playwright, que maneja mejor la carga dinámica y los entornos headless.

        # Inicializa el driver
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def extraer_comprobantes(self, datos : ParametrosExtraccion):
        # estas lineas de aqui es para probar la carga, se puede borrar si quiere 
        # return JSONResponse(
        #         status_code=200,
        #         content={"message": 'Se finalizo la descarga de comprobantes'}
        #     )
        # Paso 1: inicializa el navegador 
        driver = self.RunProfile()
        # Abre la URL deseada
        driver.get(self.url) 
        # Abrir una nueva pestaña sin cambiar a ella
        extension_url = "chrome-extension://hlifkpholllijblknnmbfagnkjneagid/popup/popup.html#/"
        driver.execute_script(f"window.open('{extension_url}', '_blank');")
        # Cambiar a la pestaña actual (la nueva)
        driver.switch_to.window(driver.window_handles[1])

        # Cerrar solo la pestaña actual
        time.sleep(1)
        driver.close()

        # Cambiar a la pestaña anterior
        driver.switch_to.window(driver.window_handles[0])

        try:
            # Paso 2: login
            driver.find_element(By.NAME, "usuario").send_keys(datos.identificacion)
            driver.find_element(By.NAME, "password").send_keys(datos.password)
            driver.find_element(By.NAME, "login").click()
            print("login ok")

            # Paso 3: Navegar a la sección de Facturación Electrónica
            time.sleep(1)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.eliminar-boton'))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "FACTURACIÓN ELECTRÓNICA")]'))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Comprobantes electrónicos recibidos")]'))).click()
            print("entramos al panel de comprobantes")
            # driver.find_element(By.XPATH, '//span[contains(text(), "Comprobantes electrónicos recibidos")]').click()
            

            # Paso 4: Seleccionar año, mes y día
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "frmPrincipal:ano")))
            Select(driver.find_element(By.NAME, "frmPrincipal:ano")).select_by_value(datos.anio)
            time.sleep(1)
            Select(driver.find_element(By.NAME, "frmPrincipal:mes")).select_by_value(datos.mes)
            time.sleep(1)
            if datos.dia != "Todos":
                Select(driver.find_element(By.NAME, "frmPrincipal:dia")).select_by_value(datos.dia)
            else:
                Select(driver.find_element(By.NAME, "frmPrincipal:dia")).select_by_visible_text("Todos")
            time.sleep(1)

            print("seleccion de parametros ok")

            # Paso 5: Hacer clic en Consultar
            driver.find_element(By.ID, "frmPrincipal:btnConsultar").click()
            time.sleep(1)
            
            print("click en consultar")

            # paso 6: Resolver reCAPTCHA si se detecta
            captcha = driver.execute_script("return document.getElementById('rc-imageselect')")
            print(captcha)
            if captcha:
                print("reCAPTCHA detectado. Resolviendo...")
                # verifica q tenga el sericio de captcha
                while True:
                    try:
                        res = driver.execute_script("return document.querySelector('.g-recaptcha').dataset['sitekey']")
                        print(res, self.key) 
                        if res == self.key:
                            break
                    except Exception as exc:
                        print(exc)
                        time.sleep(3)
            
                while True:
                    try:
                        print("resolviendo captcha")
                        user_agent = driver.execute_script("return navigator.userAgent")
                        g_recaptcha_response = driver.find_element(By.ID, "g-recaptcha-response").get_attribute("value")

                        data = {
                            'Solution': g_recaptcha_response,
                            'User-Agent': user_agent
                        }
                        if g_recaptcha_response != '':
                            break
                        else:
                            time.sleep(3)
                            
                        # si hay contenido salir del bucle
                        rows = driver.find_elements(By.CSS_SELECTOR, "div[id='frmPrincipal:tablaCompRecibidos'] table tbody tr")
                        if len(rows) > 0:
                            break
                        
                    except Exception as ex:
                        time.sleep(3)
                        print(e)
                        continue
                print("paso el captcha")
            else:
                print("No se detectó reCAPTCHA")
                # tabla_comprobantes = driver.find_elements(By.ID, "frmPrincipal:tablaCompRecibidos")
                # if not tabla_comprobantes:
                #     driver.find_element(By.ID, "btnRecaptcha").click()
                

            # verifica la existencia de altertas informativas por parte de la pagina
            alert_pagina = driver.find_element(By.ID, "formMessages:messages").text
            if alert_pagina:
                print('no hay resultados')
                respuesta = alert_pagina
            else:
                # Paso 7: Esperar a que la tabla de resultados cargue
                print("si hay resultados")
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='frmPrincipal:tablaCompRecibidos']")))

                
                # Paso 8: Crear la carpeta "comprobantes" si no existe
                if os.path.exists(self.output_dir):
                    shutil.rmtree(self.output_dir)  # Eliminar la carpeta y su contenido
                os.makedirs(self.output_dir)  # Crear una nueva carpeta vacía

                # Paso 9: Descargar los archivos XML
                rows = driver.find_elements(By.CSS_SELECTOR, "div[id='frmPrincipal:tablaCompRecibidos'] table tbody tr")
                print(len(rows), "comprobantes electrónicos recibidos")
                time.sleep(2)
                i = 0
                for row in rows:
                    try:
                        # Obtener el botón del XML
                        xml_button = row.find_element(By.CSS_SELECTOR, f"a[id='frmPrincipal:tablaCompRecibidos:{i}:lnkXml']")
                        
                        # Verificar si el botón del XML existe y hacer clic para descargar
                        if xml_button:
                            xml_button.click()  # Descargar el archivo
                            time.sleep(2)  # Esperar 1 segundos para completar la descarga
                        i += 1
                    except Exception as e:
                        print(f"Error al descargar comprobante {i+1}")
                        i += 1
                        continue
                # paso 10: verificar si se descagaron todos los comprobante
                if rows and len(rows) == i:
                    respuesta = 'Se finalizo la descarga de comprobantes'
                else:
                    respuesta = 'No se descagaron todos los comprobantes, intentalo de nuevo'
        except NoSuchElementException:
            print("El elemento no se encontró en la página.")
            respuesta = "No es posible acceder al portal de SRI, intentelo más tarde"
        except TimeoutException as e:
            print(f"El tiempo de espera se agotó")
            respuesta = "El tiempo de espera se agotó, intentelo de nuevo"
        except ElementNotInteractableException:
            print("El elemento no es interactuable.")
            respuesta = "El elemento no es interactuable por el momento, intentelo de nuevo o más tarde"
        except WebDriverException as e:
            print(f"Error general del WebDriver: {e}")
            respuesta = "Error general del WebDriver, intentelo de nuevo"
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            respuesta = "Ocurrió un error inesperado, intentelo de nuevo"
        finally:
            print("cerrando el navegador")
            # Eliminar todas las cookies
            driver.delete_all_cookies()
            # Cierra el navegador al final
            driver.quit()
        
        return JSONResponse(
                status_code=200,
                content={"message": respuesta}
            )

    def cargar_comprobantes(self, request: Request, db : Session):
        token = request.headers.get("Authorization")
        token = token.split(" ")
        payload = OptionsToken.get_info_token(token[1])
        correo = payload.get("sub")
        usuario_cuenta = self.facade.get_user_by_email(correo, db)

        for index, filename in enumerate(os.listdir(self.output_dir)):
            if filename.endswith(".xml"):
                with open(os.path.join(self.output_dir, filename), "r", encoding="utf-8") as file:
                    data = file.read()
                    xml = data.split("<![CDATA[")[1].split("]]>")[0]
                    file.close()
                    
                    root = ET.fromstring(xml)
                # datos del vendedor
                    infoTributaria = root.find('infoTributaria')
                    claveAcceso = infoTributaria.find('claveAcceso').text
                    razonSocial = infoTributaria.find('razonSocial').text
                    ruc = infoTributaria.find('ruc').text

                    infoFactura = root.find('infoFactura')
                    fechaEmision = infoFactura.find("fechaEmision").text
                    importeTotal = infoFactura.find('importeTotal').text

                # comprador
                    razonSocialComprador = infoFactura.find('razonSocialComprador').text
                    identificacionComprador = infoFactura.find('identificacionComprador').text
                    # verifico la existencia del comprador
                    if index == 0:
                        try:
                            comprador = self.facade.comprador_find_one(identificacionComprador, db)
                            if not comprador:
                                datos = CompradorCreate( 
                                    identificacion_comprador = identificacionComprador,
                                    razon_social_comprador = razonSocialComprador
                                )
                                resultado = self.facade.comprador_insert(datos, db)
                                self.cod_comprador = resultado.cod_comprador
                            else:
                                self.cod_comprador = comprador.cod_comprador
                        except Exception as e:
                            raise HTTPException(status_code=500, detail=f"Ocurrio un error en comprador {str(e)}") from e

                    detalles = root.find('detalles')
            
                    nueva_raiz = ET.Element('factura')  # Crear una nueva raíz
                    nueva_raiz.append(infoTributaria)     # Añadir hijos
                    nueva_raiz.append(infoFactura)     
                    nueva_raiz.append(detalles)  
                    # Imprimir el árbol XML completo
                    xml_string = ET.tostring(nueva_raiz, encoding='unicode', method='xml')
                    # print(xml_string)
                # comporbantes
                    try:
                        comprobante = self.facade.comprobante_find_one(claveAcceso, db)
                        if not comprobante:
                            datos_comprobante = ComprobantesCreate(
                                cod_comprador = self.cod_comprador,
                                archivo = xml_string,
                                clave_acceso = claveAcceso,
                                ruc = ruc,
                                razon_social = razonSocial,
                                fecha_emision = datetime.strptime(fechaEmision, "%d/%m/%Y"),
                                importe_total = importeTotal
                            )
                            resultado = self.facade.comprobante_insert(datos_comprobante, db)
                        
                            self.cod_comprobante = resultado.cod_comprobante

                            # detalles
                            detalle_valor = 0
                            for detalle in detalles.findall('detalle'):
                                descripcion = detalle.find("descripcion").text
                                cantidad = int(float(detalle.find("cantidad").text))
                                precioUnitario = float(detalle.find("precioUnitario").text)

                                precioTotalSinImpuesto = detalle.find("precioTotalSinImpuesto").text
                                impuesto_valor = detalle.find('impuestos').find("impuesto").find("valor").text
                                detalle_valor = float(precioTotalSinImpuesto) + float(impuesto_valor)   #?valor $ de cada detalle

                                datos_detalle = DetallesCreate(
                                    cod_categoria = 1,
                                    cod_comprobante = self.cod_comprobante,
                                    descripcion = descripcion,
                                    cantidad = cantidad,
                                    precio_unitario = precioUnitario,
                                    precio_total_sin_impuesto = precioTotalSinImpuesto,
                                    impuesto_valor = impuesto_valor,
                                    detalle_valor = detalle_valor
                                )
                                try:
                                    self.facade.detalle_insert(datos_detalle, db)
                                except Exception as e:
                                    raise HTTPException(status_code=500, detail=f"Ocurrio un error en detalles comprobrantes {str(e)}") from e
                                
                            #? descontar cantidad de comprobantes que puede cargar en sus plan de suscripcion
                            print(self.facade.descontar_cant_comprobantes(usuario_cuenta.cod_usuario, db))
                        else:
                            self.cod_comprobante = comprobante.cod_comprobante
                    except Exception as e:
                        raise HTTPException(status_code=500, detail=f"Ocurrio un error en comprobantes {str(e)}") from e
                
        
        return JSONResponse(
            status_code=200,
            content={"message": "Se finalizo la carga de comprobantes"}
        )
    
# comprobantes
    def lista_comprobantes(self, datos : ComprobantesLista, db : Session):
        resultado =self.facade.comprador_find_one(datos.identificacion, db)
        if not resultado:
            return JSONResponse(
                status_code=200,
                content={"message": "No hay datos registrados"}
            )
        try:
            datos.cod_comprador = resultado.cod_comprador
            resultado = self.facade.lista_comprobantes(datos, db)
            return resultado
        except  Exception as e:
             raise HTTPException(status_code=400, detail=f"Ocurrio un error al lista los comprobantes {e}") from e

# compradores
    def lista_compradores(self, db : Session):
        return self.facade.lista_compradores(db)

# Detalles
    def detalles_comprobante(self, cod_comprobante, db : Session):
        return self.facade.detalles_comprobante(cod_comprobante, db)
    def detalles_update(self, datos, db : Session):
        return self.facade.detalles_update(datos, db)