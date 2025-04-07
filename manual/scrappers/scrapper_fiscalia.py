import os
import time
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError

# Configurar carpeta de descargas
carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads", "Fiscalia")
Path(carpeta_descargas).mkdir(parents=True, exist_ok=True)

try:
    with sync_playwright() as p:
        # Configuración del navegador
        browser = p.chromium.launch(
            headless=False,  # Visible para depuración
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-extensions",
                "--no-sandbox",
            ]
        )
        
        # Crear un contexto de navegador personalizado
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            accept_downloads=True,
            ignore_https_errors=True
        )
        
        # Configurar comportamiento más humano
        context.set_default_timeout(90000)  # 90 segundos de tiempo de espera
        
        # Crear una nueva página
        page = context.new_page()
        
        # Evadir detección de bots
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['es-ES', 'es'] });
        """)
        
        print("Navegando a la página de la Fiscalía...")
        # Navegar a la página con reintentos
        max_intentos = 3
        for intento in range(max_intentos):
            try:
                # Abrir la página
                response = page.goto("https://www.fiscalia.gov.co/colombia/gestion/estadisticas/delitos/", 
                                    wait_until="networkidle", timeout=60000)
                if response.status == 200:
                    print(f"Página cargada correctamente (Status: {response.status})")
                    break
                else:
                    print(f"Intento {intento+1}: Status code {response.status}")
                    if intento == max_intentos - 1:
                        raise Exception(f"No se pudo cargar la página. Status: {response.status}")
                    time.sleep(5)
            except Exception as e:
                print(f"Error en intento {intento+1}: {e}")
                if intento == max_intentos - 1:
                    raise
                page.reload()
                time.sleep(5)
        
        # Esperar a que la página cargue completamente
        print("Esperando que la página termine de cargar...")
        page.wait_for_load_state("networkidle")
        time.sleep(5)  # Espera adicional para scripts asíncronos
        
        # Verificar si podemos encontrar el elemento contenedor
        print("Buscando elementos principales...")
        try:
            contenedor = page.wait_for_selector("#C_Articulo", timeout=30000)
            print("Elemento #C_Articulo encontrado")
        except TimeoutError:
            # Si no encuentra el ID específico, intentamos con un selector más general
            print("No se encontró #C_Articulo, intentando con otro selector...")
            contenedor = page.wait_for_selector(".container-fluid", timeout=30000)
            print("Contenedor general encontrado")
        
        # Examinar la estructura del select
        # Puede ser un select normal o un Select2
        try:
            # Intentar primero con Select2
            select_container = page.wait_for_selector(".select2-container", timeout=10000)
            print("Encontrado widget Select2")
            
            # Hacer clic para abrir las opciones
            select_container.click()
            time.sleep(2)
            
            # Obtener todas las opciones disponibles
            opciones = page.query_selector_all(".select2-results li")
            
            if not opciones:
                print("No se encontraron opciones en Select2, buscando select nativo...")
                page.click("body")  # Cerrar el dropdown de Select2
                select_element = page.wait_for_selector("select", timeout=10000)
                opciones = select_element.query_selector_all("option")
                es_select_nativo = True
            else:
                es_select_nativo = False
                
            print(f"Encontradas {len(opciones)} opciones")
            
            # Si no hay opciones, intentamos otra estrategia
            if not opciones:
                raise Exception("No se pudieron encontrar opciones en el selector")
            
            # Para cada opción
            for i, opcion in enumerate(opciones):
                # Obtener el texto de la opción para nombrar el archivo
                if es_select_nativo:
                    texto_opcion = opcion.inner_text().strip()
                    if not texto_opcion or opcion.get_attribute("value") == "":
                        continue  # Saltar opciones vacías
                        
                    # Seleccionar la opción mediante JavaScript
                    page.evaluate(f"document.querySelector('select').value = '{opcion.get_attribute('value')}'")
                    page.evaluate("document.querySelector('select').dispatchEvent(new Event('change'))")
                else:
                    # Reabrir el dropdown de Select2
                    select_container.click()
                    time.sleep(1)
                    
                    # Refrescar las opciones (pueden haber cambiado en el DOM)
                    opciones_actualizadas = page.query_selector_all(".select2-results li")
                    if i >= len(opciones_actualizadas):
                        print(f"Índice {i} fuera de rango, hay {len(opciones_actualizadas)} opciones")
                        continue
                        
                    texto_opcion = opciones_actualizadas[i].inner_text().strip()
                    if not texto_opcion:
                        continue
                        
                    # Hacer clic en la opción
                    opciones_actualizadas[i].click()
                
                # Limpiar el texto para usarlo como nombre de archivo
                nombre_archivo = re.sub(r'[\\/*?:"<>|]', "", texto_opcion).strip()
                print(f"Procesando opción: '{nombre_archivo}'")
                
                # Esperar a que se actualicen los datos
                time.sleep(5)
                
                # Buscar y hacer clic en el botón de exportación
                try:
                    boton_exportar = page.wait_for_selector("#P_Anios_new .exportButton", timeout=10000)
                    
                    # Asegurarse que el botón es visible
                    page.evaluate("arguments[0].scrollIntoView({block: 'center'})", boton_exportar)
                    time.sleep(1)
                    
                    print("Haciendo clic en botón de exportación...")
                    
                    # Configurar manejo de descarga
                    with page.expect_download() as download_info:
                        boton_exportar.click()
                    
                    # Esperar y guardar la descarga
                    download = download_info.value
                    print(f"Descarga iniciada: {download.suggested_filename}")
                    
                    # Establecer nombre personalizado
                    if download.suggested_filename:
                        extension = os.path.splitext(download.suggested_filename)[1]
                        ruta_archivo = os.path.join(carpeta_descargas, f"{nombre_archivo}{extension}")
                    else:
                        ruta_archivo = os.path.join(carpeta_descargas, f"{nombre_archivo}.xlsx")
                    
                    # Guardar archivo con el nombre personalizado
                    download.save_as(ruta_archivo)
                    print(f"Archivo guardado como: {ruta_archivo}")
                    
                except TimeoutError:
                    print(f"No se encontró el botón de exportación para la opción '{nombre_archivo}'")
                except Exception as e:
                    print(f"Error al descargar para la opción '{nombre_archivo}': {e}")
                
                # Esperar antes de procesar la siguiente opción
                time.sleep(3)
                
        except Exception as e:
            print(f"Error al procesar opciones: {e}")
            import traceback
            traceback.print_exc()
            
        # Cerrar el navegador
        context.close()
        browser.close()
        print("Navegador cerrado correctamente")

except Exception as e:
    print(f"Error general: {e}")
    import traceback
    traceback.print_exc()
