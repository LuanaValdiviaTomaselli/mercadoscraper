from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import sys
import os
import time
import csv


def iniciar_chrome():
    ruta = ChromeDriverManager().install()

    options = Options()

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.3"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxi-server")
    options.add_argument("--disable-blink-features=AutomationControlled")

    ex_opt = ["enable-automation", "ignore-certificate-errors", "enable-logging"]
    options.add_experimental_option("excludeSwitches", ex_opt)

    prefs = { "profilde.default_content_setting_values.notifications" : 2,
              "Intl.accept_lenguajes" : "ES-es,es",
              "credentials_enable_service" : False
            }
    options.add_experimental_option("prefs", prefs)
    

    s = Service(ruta)
    driver = webdriver.Chrome(service=s, options=options)

    return driver



def buscaprod(producto, minimo):
    try:
        driver = iniciar_chrome()
    except Exception as e:
        print(f"Error al inicializar chrome: {str(e)}")
        return

    print(f'Buscando producto: {producto}')
    driver.get(f'https://listado.mercadolibre.com.ar/{producto}')
    
    prodinfo = []
    scrolls = 11
    intentos_fallidos = 0
    MAX_INTENTOS = 3  # Máximo de páginas vacías permitidas

    while len(prodinfo) < minimo and intentos_fallidos < MAX_INTENTOS:
        try:
            # Esperar a que carguen los productos
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.poly-card__content"))
            )
            
            # Scroll progresivo
            for _ in range(3):
                driver.execute_script("window.scrollBy(0, window.innerHeight/2)")
                time.sleep(random.uniform(0.5, 1.5))
                
            # Extraer productos
            productos = driver.find_elements(By.CSS_SELECTOR, "div.poly-card__content")
            
            if not productos:
                print(f"No se encontraron productos en la página (Intento {intentos_fallidos}/{MAX_INTENTOS})")
                time.sleep(2)
                break
                
            #intentos_fallidos = 0  # Resetear contador si encontró productos
            
            for product in productos:
                try:
                    nombre = product.find_element(By.CSS_SELECTOR, "h3.poly-component__title-wrapper")
                    preciocomp = product.find_element(By.CSS_SELECTOR, "div.poly-price__current")
                    precio = '$' + preciocomp.find_element(By.CSS_SELECTOR, "span.andes-money-amount__fraction").text.strip()
                    link = nombre.find_element(By.CSS_SELECTOR, "a.poly-component__title").get_attribute("href").strip()
                    
                    # Rating es opcional
                    try:
                        rating = product.find_element(By.CSS_SELECTOR, "span.poly-component__reviews").text
                    except:
                        rating = "Sin rating"
                        
                    prodinfo.append((nombre.text.strip(), precio, rating, link))
                    
                    if len(prodinfo) >= minimo:
                        break
                        
                except Exception as e:
                    print(f"Error procesando un producto: {str(e)}")
                    continue
            
            print(f'Productos recolectados: {len(prodinfo)}/{minimo}')
            
            # Paginación, primero me fijo si ya llego al boton o no.
            if scrolls == 11:
                try:
                    nextbutton = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.andes-pagination__button--next a"))
                    )
                    #uso js para que no me de errores visuales al hacer las cosas tan rapido
                    driver.execute_script("arguments[0].click();", nextbutton)
                    time.sleep(random.uniform(2, 4)) 
                # Espera aleatoria 
                except:
                    print("No se pudo clickear el boton")
                 
            else:
                continue
            #sumo scrolls por cada ejecucion del while
            scrolls += 1
                    
        except Exception as e:
            print(f"Error en el bucle principal: {str(e)}")
            intentos_fallidos += 1
            time.sleep(2)

    # Guardar resultados
    if prodinfo:
        with open("productos.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(('Nombre', 'Precio', 'Rating', 'URL'))
            writer.writerows(prodinfo)
        print(f"Archivo guardado con {len(prodinfo)} productos")
    else:
        print("No se encontraron productos")

    driver.quit()


if __name__ == '__main__':

    mododeuso = f'Modo de uso\n'
    mododeuso += f' {os.path.basename(sys.executable)}{sys.argv[0]} hashtag [minimo]\n\n'
    mododeuso += f' opciones:\n'
    mododeuso += f' minimo : minino de descargas a realizar (por defecto 300)\n\n'
    mododeuso += f'{os.path.basename(sys.executable)} {sys.argv[0]} cats\n'
    mododeuso += f'{os.path.basename(sys.executable)} {sys.argv[0]} superman\n'
    # control e parametros
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print(mododeuso)
        sys.exit(1)
    elif len(sys.argv) == 3:
        if sys.argv[2].isdigit():
            minimo = int(sys.argv[2])
        else:
            print(f'Error: {sys.argv[2]} no es un numero')
            sys.exit(1)
    else:
        minimo=300
    producto = sys.argv[1].strip().lower()

    buscaprod(producto, minimo)


