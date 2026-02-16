<div align="center">

# ⚡ Visual Gallery Explorer Pro

### Busca, explora y descarga imágenes de la web con estilo

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-Desktop_App-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/Licencia-MIT-6c63ff?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Versión-5.0-00d4aa?style=for-the-badge)]()

<br>

```
╔══════════════════════════════════════════════════════════════╗
║  ⚡ Visual Gallery Explorer          [PRO]    📷 12 imágenes ║
╠══════════════════════════════════════════════════════════════╣
║  🔍 Buscador  │  🖼 Galería  │  ✨ Acerca de                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │  🔍 Buscar imágenes                                     │ ║
║  │                                                         │ ║
║  │  [Google ▼]  [ Escribe qué quieres buscar...  ]  🚀    │ ║
║  │  ─────────────────────────────────────────────────────  │ ║
║  │  📐 Tamaño [Cualquier ▼]  🎨 Color [Cualquier ▼]  🛡️  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │  📷 Resultados                              [24]        │ ║
║  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐               │ ║
║  │  │ 🖼️  │  │ 🖼️  │  │ 🖼️  │  │ 🖼️  │               │ ║
║  │  │      │  │      │  │      │  │      │               │ ║
║  │  └──────┘  └──────┘  └──────┘  └──────┘               │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💡 Listo para buscar                                        ║
╚══════════════════════════════════════════════════════════════╝
```

<br>

*Una aplicación de escritorio moderna y elegante para buscar, explorar y descargar imágenes desde múltiples motores de búsqueda.*

</div>

---

## ✨ Características

<table>
<tr>
<td width="50%" valign="top">

### 🔍 Búsqueda Multi-Motor
Busca imágenes simultáneamente en **Google**, **Bing** y **DuckDuckGo**. Cambia de motor con un solo clic.

### 🎨 Filtros Avanzados
Filtra por **tamaño** (grande, mediano, pequeño), **color** (B/N, transparente, RGB) y activa **SafeSearch**.

### 📥 Descarga Masiva
Selecciona múltiples imágenes y descárgalas todas a la vez con barra de progreso en tiempo real.

</td>
<td width="50%" valign="top">

### 🖼 Galería Inteligente
Galería local con miniaturas, nombre de archivo, tamaño y acceso rápido a detalles.

### 🎬 Slideshow Inmersivo
Presentación a pantalla completa con controles de velocidad, contador de posición y navegación por teclado.

### ⚡ Rendimiento Asíncrono
Búsqueda, descarga y carga de miniaturas en **hilos secundarios**. La interfaz nunca se congela.

</td>
</tr>
</table>

---

## 🏗️ Arquitectura del Proyecto

El código está organizado en módulos separados siguiendo el principio de responsabilidad única:

```
PyPhotoScraper/
├── 🚀 main.py                  # Punto de entrada de la aplicación
├── 📄 interfaces.py             # Compatibilidad (redirige a main.py)
├── 📋 requirements.txt          # Dependencias del proyecto
├── 📜 LICENSE                   # Licencia MIT
│
├── 🎨 ui/                      # Capa de interfaz de usuario
│   ├── __init__.py
│   ├── styles.py                # 🎨 Tema, colores, estilos CSS
│   └── main_window.py           # 🖥️ Ventana principal y lógica UI
│
├── ⚙️ workers/                  # Hilos en segundo plano
│   ├── __init__.py
│   ├── search_worker.py         # 🔍 Búsqueda de imágenes (QThread)
│   └── download_worker.py       # 📥 Descarga + carga de thumbnails
│
├── 🖼️ Imagenes/                 # Carpeta de imágenes descargadas
└── 📦 assets/                   # Recursos gráficos
```

### Diagrama de flujo

```
┌──────────────┐     señales Qt      ┌──────────────────┐
│  main.py     │────────────────────▶│  MainWindow      │
│  (entrada)   │                     │  (ui/main_window) │
└──────────────┘                     └────────┬─────────┘
                                              │
                              ┌───────────────┼───────────────┐
                              ▼               ▼               ▼
                     ┌──────────────┐ ┌──────────────┐ ┌────────────┐
                     │ SearchWorker │ │  Downloader  │ │ Thumbnail  │
                     │  (QThread)   │ │  (QThread)   │ │  Loader    │
                     └──────┬───────┘ └──────┬───────┘ └─────┬──────┘
                            │                │               │
                            ▼                ▼               ▼
                     ┌──────────────────────────────────────────────┐
                     │          Internet (HTTP requests)            │
                     │   Google  ·  Bing  ·  DuckDuckGo            │
                     └──────────────────────────────────────────────┘
```

---

## 🚀 Instalación

### Requisitos previos

- **Python 3.8** o superior
- **pip** (gestor de paquetes de Python)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/JesusCaRu/PyPhotoScraper.git
cd PyPhotoScraper

# 2. (Opcional) Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## ▶️ Uso

```bash
python main.py
```

### Guía rápida

| Paso | Acción | Descripción |
|:----:|--------|-------------|
| **1** | 🔍 Buscar | Escribe un término y pulsa **Enter** o el botón **Buscar** |
| **2** | 🎨 Filtrar | Ajusta tamaño, color y SafeSearch antes de buscar |
| **3** | ☑️ Seleccionar | Haz clic en las imágenes o marca los checkboxes |
| **4** | 📥 Descargar | Pulsa **Descargar** para guardarlas en `/Imagenes` |
| **5** | 🖼 Galería | Cambia a la pestaña Galería para ver tu colección |
| **6** | 🎬 Slideshow | Inicia una presentación a pantalla completa |

### Atajos

| Atajo | Acción |
|-------|--------|
| `Enter` | Buscar imágenes |
| `Escape` | Cerrar slideshow |
| `Click` en imagen (búsqueda) | Seleccionar / deseleccionar |
| `Click` en imagen (galería) | Ver detalles |

---

## 🧩 Dependencias

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| [PyQt5](https://pypi.org/project/PyQt5/) | ≥ 5.15 | Framework GUI de escritorio |
| [requests](https://pypi.org/project/requests/) | ≥ 2.25 | Peticiones HTTP |
| [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) | ≥ 4.9 | Parsing HTML (web scraping) |
| [Pillow](https://pypi.org/project/Pillow/) | ≥ 8.0 | Procesamiento de imágenes |

---

## 🎨 Diseño

La interfaz utiliza un **tema oscuro premium** inspirado en aplicaciones modernas como Discord y Figma:

| Elemento | Color | Uso |
|----------|-------|-----|
| 🟣 `#6c63ff` | Violeta | Acento principal, botones primarios |
| 🟢 `#00d4aa` | Cian | Éxito, gradientes, progreso |
| 🔵 `#1a1f2e` | Azul oscuro | Fondo principal |
| ⚫ `#0d1017` | Negro profundo | Fondo del slideshow |
| 🟡 `#ffb347` | Ámbar | Warnings |
| 🔴 `#ff6b6b` | Rosa | Errores, botón limpiar |

### Variantes de botón

- **Primary** — Gradiente violeta → cian (acciones principales)
- **Accent** — Violeta sólido (acciones secundarias)
- **Ghost** — Transparente con borde (acciones opcionales)
- **Danger** — Borde rojo (acciones destructivas)

---

## 🔧 Decisiones Técnicas

### ¿Por qué QThread y no `asyncio`?
PyQt5 tiene su propio event loop incompatible con `asyncio`. Los `QThread` permiten ejecutar tareas pesadas (HTTP requests) sin bloquear la UI, comunicándose vía señales Qt thread-safe.

### ¿Por qué los thumbnails se cargan como bytes y no como QPixmap?
**`QPixmap` no se puede crear fuera del hilo principal** en Qt. El worker descarga las imágenes como bytes crudos y emite una señal; el slot en el hilo principal crea el `QPixmap`. Esto evita crashes aleatorios.

### ¿Por qué no se usan variables CSS (`var(--color)`)?
PyQt5 **no soporta** variables CSS nativas. Todos los colores están centralizados como constantes Python en `ui/styles.py` y se insertan mediante f-strings.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Sigue estos pasos:

```bash
# 1. Fork del repositorio

# 2. Crear rama de feature
git checkout -b feature/mi-mejora

# 3. Hacer commits
git commit -m "feat: descripción de la mejora"

# 4. Push y crear Pull Request
git push origin feature/mi-mejora
```

### Ideas para contribuir

- [ ] 🌍 Internacionalización (i18n) — soporte multi-idioma
- [ ] 🔄 Paginación — cargar más resultados con scroll infinito
- [ ] 🏷️ Etiquetas — organizar imágenes por categorías
- [ ] 🌙 Modo claro — tema alternativo
- [ ] 📱 Layout responsive — adaptarse a ventanas más pequeñas
- [ ] 🔌 Proxy support — rotación de proxies para evitar bloqueos

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** — libre para uso personal y comercial.

Ver el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**Desarrollado con ❤️ por [Jesús](https://github.com/JesusCaRu)**

⚡ Si te gusta este proyecto, ¡dale una ⭐ en GitHub!

<br>

[![GitHub](https://img.shields.io/badge/Ver_en-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/JesusCaRu/PyPhotoScraper)

</div>