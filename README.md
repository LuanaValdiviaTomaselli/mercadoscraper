# 🛒 mercadoScraper

Un scraper automatizado para MercadoLibre Argentina que busca lo primeros productos que aparecen según una palabra clave y guarda los resultados en un archivo CSV. Ideal para investigaciones de precios, estudios de mercado o tareas de automatización web.

---

## 🚀 ¿Qué hace este script?

- Busca productos en [MercadoLibre Argentina](https://listado.mercadolibre.com.ar/) según una palabra clave.
- Recolecta:
  - Nombre del producto
  - Precio
  - Calificación (si está disponible)
  - URL directa al producto
- Navega entre páginas automáticamente hasta alcanzar la cantidad mínima de productos deseada.
- Guarda los resultados en un archivo `productos.csv`.

---

## 🧰 Requisitos

- Python 3.11
- Google Chrome
- ChromeDriver compatible con tu versión de Chrome
- También necesitás descargar chromedriver y asegurarte de que esté en tu PATH o en la misma carpeta del script.

### 📦 Librerías necesarias:

```bash
pip install selenium
