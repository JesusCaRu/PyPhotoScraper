# 📸 PyPhotoScraper

## Descripción
PyPhotoScraper es una aplicación de escritorio desarrollada en Python que permite descargar y organizar imágenes de manera automatizada utilizando técnicas de web scraping. La aplicación cuenta con una interfaz gráfica intuitiva que facilita la búsqueda, descarga y gestión de imágenes desde diferentes fuentes web.

## Características principales
- 🔍 Búsqueda avanzada de imágenes en múltiples sitios web
- 📥 Descarga automática de imágenes en alta resolución
- 🗂️ Organización de imágenes por categorías y etiquetas
- 🖼️ Visualización de imágenes en modo galería o detalle
- 🔄 Funcionalidad de actualización para mantener la colección al día

## Estructura del proyecto
```
PyPhotoScraper/
├── interfaces.py       # Interfaz gráfica y lógica principal
├── assets/             # Recursos gráficos e iconos
│   ├── checkbox-checked.svg
│   ├── checkbox-unchecked.svg
│   ├── gallery.png
│   ├── gallery.svg
│   └── view-details.png
└── Imagenes/           # Directorio para almacenar las imágenes descargadas
```

## Instalación
1. Clona este repositorio:
```bash
git clone https://github.com/JesusCaRu/PyPhotoScraper.git
```

2. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

## Uso
Ejecuta el archivo principal para iniciar la aplicación:
```bash
python interfaces.py
```

## Dependencias
- Python 3.6+
- PyQt5 (para la interfaz gráfica)
- Requests (para realizar peticiones HTTP)
- BeautifulSoup4 (para el web scraping)
- Pillow (para el procesamiento de imágenes)

## Contribuir
Las contribuciones son bienvenidas. Por favor, siente libre de enviar un Pull Request o abrir un Issue si encuentras algún problema o tienes sugerencias para mejorar la aplicación.

## Licencia
Este proyecto está licenciado bajo la licencia MIT - ver el archivo LICENSE para más detalles.

---
⭐ Si te gusta este proyecto, no dudes en dejarnos una estrella ⭐