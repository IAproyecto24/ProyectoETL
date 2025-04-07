import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

# Configurar opciones de Chrome
opciones_chrome = Options()
carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads", "Fiscalia")
if not os.path.exists(carpeta_descargas):
    os.makedirs(carpeta_descargas)

# Configuraciones adicionales para evitar detección de automatización
opciones_chrome.add_argument("--disable-blink-features=AutomationControlled")
opciones_chrome.add_argument("--disable-extensions")
opciones_chrome.add_argument("--no-sandbox")
opciones_chrome.add_argument("--disable-dev-shm-usage")
opciones_chrome.add_experimental_option("excludeSwitches", ["enable-automation"])
opciones_chrome.add_experimental_option("useAutomationExtension", False)
opciones_chrome.add_experimental_option("prefs", {
    "download.default_directory": carpeta_descargas,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    # Desactivar componentes que podrían usar tensores dinámicos
    "hardware_acceleration_mode.enabled": False
})

# Función para reintentar operaciones que podrían fallar debido a elementos obsoletos
def con_reintento(funcion, max_intentos=5):
    for intento in range(max_intentos):
        try:
            return funcion()
        except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            if intento == max_intentos - 1:
                raise
            print(f"Reintentando operación... ({intento+1}/{max_intentos})")
            time.sleep(1)

try:
    # Inicializar el navegador con configuración mejorada
    servicio = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servicio, options=opciones_chrome)
    
    # Agregar JavaScript para evitar detección de bot
    navegador.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Navegar a la página con timeout aumentado
    navegador.set_page_load_timeout(60)  # 60 segundos para cargar la página
    navegador.get("https://www.fiscalia.gov.co/colombia/gestion/estadisticas/delitos/")
    
    # Usar un método más robusto para esperar la carga completa de la página
    WebDriverWait(navegador, 60).until(
        EC.presence_of_element_located((By.ID, "C_Articulo"))
    )
    print("Página cargada correctamente")
    
    # Dar tiempo adicional para que todos los scripts se carguen
    time.sleep(5)
    
    # Intentar usar directamente el select nativo si es posible
    try:
        # Buscar el select original (sin select2)
        select_element = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#C_Articulo select"))
        )
        select = Select(select_element)
        opciones = select.options
        textos_opciones = [opcion.text for opcion in opciones]
        
        print(f"Encontradas {len(textos_opciones)} opciones en el select nativo")
        
        # Usar el select nativo
        for texto_opcion in textos_opciones:
            if not texto_opcion.strip():  # Ignorar opciones vacías
                continue
                
            print(f"Seleccionando opción: '{texto_opcion}'")
            select.select_by_visible_text(texto_opcion)
            time.sleep(3)  # Esperar actualización del contenido
            
            # Intentar encontrar y hacer clic en el botón de exportación
            boton_exportar = WebDriverWait(navegador, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#P_Anios_new .exportButton"))
            )
            
            # Desplazarse al botón para asegurarse de que es visible
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_exportar)
            time.sleep(1)
            
            print("Haciendo clic en botón de exportación")
            con_reintento(lambda: boton_exportar.click())
            
            # Esperar a que se complete la descarga
            time.sleep(8)
            
            # Renombrar archivo
            archivos = os.listdir(carpeta_descargas)
            if archivos:
                archivos = [os.path.join(carpeta_descargas, f) for f in archivos]
                ultimo_archivo = max(archivos, key=os.path.getctime)
                
                # Limpiar el nombre para el archivo
                nombre_limpio = re.sub(r'[\\/*?:"<>|]', "", texto_opcion).strip()
                _, extension = os.path.splitext(ultimo_archivo)
                nuevo_nombre = os.path.join(carpeta_descargas, f"{nombre_limpio}{extension}")
                
                os.rename(ultimo_archivo, nuevo_nombre)
                print(f"Archivo descargado y renombrado: {nuevo_nombre}")
    
    except Exception as e:
        print(f"Error usando select nativo: {e}")
        print("Intentando con select2...")
        
        # Si falla el método anterior, usar la interacción con select2
        # Encuentro el contenedor select2
        select2_container = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".select2-container"))
        )
        
        # Hacer clic para abrir las opciones
        con_reintento(lambda: select2_container.click())
        time.sleep(2)
        
        # Obtener todas las opciones
        opciones_select2 = WebDriverWait(navegador, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".select2-results li"))
        )
        
        # Guardar los textos
        textos_opciones = []
        for opcion in opciones_select2:
            texto = opcion.text.strip()
            if texto:  # Solo incluir opciones no vacías
                textos_opciones.append(texto)
        
        print(f"Encontradas {len(textos_opciones)} opciones en select2")
        
        # Cerrar el dropdown actual
        navegador.execute_script("document.body.click()")
        time.sleep(1)
        
        # Para cada opción
        for texto_opcion in textos_opciones:
            print(f"Procesando opción: '{texto_opcion}'")
            
            # Abrir el dropdown
            con_reintento(lambda: select2_container.click())
            time.sleep(2)
            
            # Encontrar y hacer clic en la opción específica
            xpath_opcion = f"//li[contains(@class, 'select2-result') and contains(text(), '{texto_opcion}')]"
            opcion = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_opcion))
            )
            con_reintento(lambda: opcion.click())
            
            # Esperar a que se actualice el contenido
            time.sleep(5)
            
            # Buscar y hacer clic en el botón de exportación
            boton_exportar = WebDriverWait(navegador, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#P_Anios_new .exportButton"))
            )
            
            # Desplazarse al botón
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_exportar)
            time.sleep(1)
            
            print("Haciendo clic en botón de exportación")
            con_reintento(lambda: boton_exportar.click())
            
            # Esperar a que se complete la descarga
            time.sleep(8)
            
            # Renombrar archivo
            archivos = os.listdir(carpeta_descargas)
            if archivos:
                archivos = [os.path.join(carpeta_descargas, f) for f in archivos]
                ultimo_archivo = max(archivos, key=os.path.getctime)
                
                # Limpiar el nombre para el archivo
                nombre_limpio = re.sub(r'[\\/*?:"<>|]', "", texto_opcion).strip()
                _, extension = os.path.splitext(ultimo_archivo)
                nuevo_nombre = os.path.join(carpeta_descargas, f"{nombre_limpio}{extension}")
                
                os.rename(ultimo_archivo, nuevo_nombre)
                print(f"Archivo descargado y renombrado: {nuevo_nombre}")

except Exception as e:
    print(f"Ocurrió un error general: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # Cerrar el navegador al finalizar
    try:
        if 'navegador' in locals():
            navegador.quit()
            print("Navegador cerrado correctamente")
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")
