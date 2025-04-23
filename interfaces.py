import sys
import os
import requests
import webbrowser
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QLabel, QFileDialog, QScrollArea, QGridLayout, QCheckBox, QMessageBox, 
    QFrame, QDialog, QDialogButtonBox, QTabWidget, QSizePolicy, QComboBox,
    QMenuBar,
    QProgressBar, QSlider, QSpinBox, QGroupBox, QMenu, QAction
)
from PyQt5.QtGui import (
    QPixmap, QFont, QIcon, QCursor, QDesktopServices, QColor, QPainter, 
    QLinearGradient, QFontDatabase, QPalette
)
from PyQt5.QtCore import Qt, QUrl, QRect, QSize, QTimer
from io import BytesIO
from PIL import Image
import random

class ModernImageScraper(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Visual Gallery Explorer Pro')
        self.setWindowIcon(QIcon('gallery.png'))
        self.resize(1920, 1080)
        
        # Cargar fuentes personalizadas
        self.load_fonts()
        
        # Configurar estilo avanzado
        self.setup_styles()
        
        # Variables de estado
        self.image_checkboxes = []
        self.image_urls = []
        self.current_search = ""
        self.download_folder = "Imagenes"
        
        # Configuración inicial
        self.setup_ui()
        
        # Cargar galería al iniciar
        QTimer.singleShot(100, self.load_local_gallery)
        
    def load_fonts(self):
        # Puedes añadir fuentes personalizadas aquí
        QFontDatabase.addApplicationFont("assets/fonts/Roboto-Regular.ttf")
        QFontDatabase.addApplicationFont("assets/fonts/Roboto-Bold.ttf")
        
    def setup_styles(self):
        # Estilo avanzado con variables CSS
        self.setStyleSheet("""
            :root {
                --primary: #4fc1ff;
                --primary-dark: #3aa7e6;
                --secondary: #2a2e36;
                --text: #e0e3e7;
                --text-secondary: #a0a5b0;
                --bg: #1e2127;
                --bg-dark: #17191e;
                --card-bg: #2a2e36;
                --card-border: #3a3f4b;
                --success: #4caf50;
                --warning: #ff9800;
                --error: #f44336;
            }
            
            QWidget {
                background-color: var(--bg);
                color: var(--text);
                font-family: 'Roboto', 'Segoe UI', sans-serif;
            }
            
            QTabWidget::pane {
                border: none;
                background: transparent;
                margin-top: 10px;
            }
            
            QTabBar::tab {
                background: var(--secondary);
                color: var(--text-secondary);
                padding: 12px 24px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
                font-size: 14px;
                font-weight: 500;
                border: none;
                transition: all 0.2s;
            }
            
            QTabBar::tab:selected {
                background: var(--card-bg);
                color: white;
                border-bottom: 3px solid var(--primary);
            }
            
            QTabBar::tab:hover {
                background: #323842;
            }
            
            QLineEdit {
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 6px;
                padding: 12px 16px;
                font-size: 16px;
                color: var(--text);
                selection-background-color: var(--primary);
            }
            
            QLineEdit:focus {
                border: 2px solid var(--primary);
            }
            
            QPushButton {
                background: var(--card-bg);
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                color: var(--text);
                min-width: 100px;
                transition: all 0.2s;
            }
            
            QPushButton:hover {
                background: #323842;
                transform: translateY(-1px);
            }
            
            QPushButton:pressed {
                background: var(--secondary);
                transform: translateY(1px);
            }
            
            QPushButton#primary {
                background: var(--primary);
                color: var(--bg-dark);
                font-weight: 600;
            }
            
            QPushButton#primary:hover {
                background: var(--primary-dark);
            }
            
            QPushButton#primary:pressed {
                background: #2e96c9;
            }
            
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            QCheckBox {
                spacing: 8px;
                color: var(--text);
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid var(--card-border);
                border-radius: 4px;
            }
            
            QCheckBox::indicator:checked {
                background: var(--primary);
                border: 2px solid var(--primary);
            }
            
            QProgressBar {
                border: 1px solid var(--card-border);
                border-radius: 4px;
                text-align: center;
                background: var(--secondary);
            }
            
            QProgressBar::chunk {
                background: var(--primary);
                width: 10px;
            }
            
            QComboBox {
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 120px;
            }
            
            QComboBox:hover {
                border: 1px solid var(--primary);
            }
            
            QComboBox::drop-down {
                border: none;
            }
            
            QGroupBox {
                border: 1px solid var(--card-border);
                border-radius: 8px;
                margin-top: 20px;
                padding-top: 15px;
                font-weight: bold;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        # Configurar paleta de colores oscuros
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 33, 39))
        palette.setColor(QPalette.WindowText, QColor(224, 227, 231))
        palette.setColor(QPalette.Base, QColor(42, 46, 54))
        palette.setColor(QPalette.AlternateBase, QColor(42, 46, 54))
        palette.setColor(QPalette.ToolTipBase, QColor(224, 227, 231))
        palette.setColor(QPalette.ToolTipText, QColor(224, 227, 231))
        palette.setColor(QPalette.Text, QColor(224, 227, 231))
        palette.setColor(QPalette.Button, QColor(58, 63, 75))
        palette.setColor(QPalette.ButtonText, QColor(224, 227, 231))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(79, 193, 255))
        palette.setColor(QPalette.Highlight, QColor(79, 193, 255))
        palette.setColor(QPalette.HighlightedText, QColor(26, 29, 35))
        QApplication.setPalette(palette)
        
    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        self.setLayout(self.main_layout)
        
        # Crear barra de menú
        self.setup_menu_bar()
        
        # Layout principal con pestañas
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setDocumentMode(True)
        
        # Pestaña de búsqueda
        self.search_tab = QWidget()
        self.setup_search_tab()
        self.tabs.addTab(self.search_tab, "🔍 Buscador")
        
        # Pestaña de galería
        self.gallery_tab = QWidget()
        self.setup_gallery_tab()
        self.tabs.addTab(self.gallery_tab, "🖼️ Galería")
        
        # Pestaña de información
        self.about_tab = QWidget()
        self.setup_about_tab()
        self.tabs.addTab(self.about_tab, "ℹ️ Información")
        
        self.main_layout.addWidget(self.tabs)
        
        # Barra de estado
        self.status_bar = QLabel("Listo")
        self.status_bar.setStyleSheet("""
            font-size: 12px;
            color: var(--text-secondary);
            padding: 8px;
            border-top: 1px solid var(--card-border);
        """)
        self.main_layout.addWidget(self.status_bar)
        
    def setup_menu_bar(self):
        menubar = QMenuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu("Archivo")
        
        new_search_action = QAction("Nueva búsqueda", self)
        new_search_action.triggered.connect(self.clear_search)
        file_menu.addAction(new_search_action)
        
        open_folder_action = QAction("Abrir carpeta de descargas", self)
        open_folder_action.triggered.connect(self.open_download_folder)
        file_menu.addAction(open_folder_action)
        
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Herramientas
        tools_menu = menubar.addMenu("Herramientas")
        
        settings_action = QAction("Configuración", self)
        tools_menu.addAction(settings_action)
        
        # Menú Ayuda
        help_menu = menubar.addMenu("Ayuda")
        
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        self.layout().setMenuBar(menubar)
        
    def setup_search_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        self.search_tab.setLayout(layout)
        
        # Grupo de búsqueda
        search_group = QGroupBox("Búsqueda de imágenes")
        search_layout = QVBoxLayout()
        search_group.setLayout(search_layout)
        
        # Barra de búsqueda
        search_bar_layout = QHBoxLayout()
        
        self.search_type = QComboBox()
        self.search_type.addItems(["Google", "Bing", "DuckDuckGo"])
        self.search_type.setCurrentIndex(0)
        search_bar_layout.addWidget(self.search_type)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar imágenes...")
        self.search_input.setClearButtonEnabled(True)
        search_bar_layout.addWidget(self.search_input, 1)
        
        self.search_btn = QPushButton("Buscar")
        self.search_btn.setObjectName("primary")
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_btn.clicked.connect(self.search_images)
        search_bar_layout.addWidget(self.search_btn)
        
        search_layout.addLayout(search_bar_layout)
        
        # Opciones de búsqueda
        options_layout = QHBoxLayout()
        
        self.size_combo = QComboBox()
        self.size_combo.addItems(["Cualquier tamaño", "Grande", "Mediano", "Pequeño"])
        options_layout.addWidget(self.size_combo)
        
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Cualquier color", "Blanco y negro", "Transparente", "Rojo", "Azul", "Verde"])
        options_layout.addWidget(self.color_combo)
        
        self.safe_search = QCheckBox("SafeSearch")
        self.safe_search.setChecked(True)
        options_layout.addWidget(self.safe_search)
        
        options_layout.addStretch()
        search_layout.addLayout(options_layout)
        
        layout.addWidget(search_group)
        
        # Grupo de resultados
        results_group = QGroupBox("Resultados")
        results_layout = QVBoxLayout()
        results_group.setLayout(results_layout)
        
        # Controles de resultados
        results_controls = QHBoxLayout()
        
        self.select_all = QPushButton("Seleccionar todo")
        self.select_all.clicked.connect(self.toggle_select_all)
        results_controls.addWidget(self.select_all)
        
        self.download_btn = QPushButton("📥 Descargar seleccionadas")
        self.download_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.download_btn.clicked.connect(self.download_selected)
        results_controls.addWidget(self.download_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        results_controls.addWidget(self.progress_bar)
        
        results_layout.addLayout(results_controls)
        
        # Área de resultados
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.results_container = QWidget()
        self.results_grid = QGridLayout()
        self.results_grid.setSpacing(20)
        self.results_grid.setContentsMargins(10, 10, 10, 10)
        self.results_container.setLayout(self.results_grid)
        
        self.scroll_area.setWidget(self.results_container)
        results_layout.addWidget(self.scroll_area)
        
        layout.addWidget(results_group)
        
    def setup_gallery_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        self.gallery_tab.setLayout(layout)
        
        # Controles de galería
        gallery_controls = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_btn.clicked.connect(self.load_local_gallery)
        gallery_controls.addWidget(self.refresh_btn)
        
        self.slideshow_btn = QPushButton("🎬 Iniciar slideshow")
        self.slideshow_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.slideshow_btn.clicked.connect(self.toggle_slideshow)
        gallery_controls.addWidget(self.slideshow_btn)
        
        self.slideshow_speed = QSlider(Qt.Horizontal)
        self.slideshow_speed.setRange(1, 10)
        self.slideshow_speed.setValue(3)
        self.slideshow_speed.setTickInterval(1)
        self.slideshow_speed.setTickPosition(QSlider.TicksBelow)
        gallery_controls.addWidget(QLabel("Velocidad:"))
        gallery_controls.addWidget(self.slideshow_speed)
        
        gallery_controls.addStretch()
        layout.addLayout(gallery_controls)
        
        # Área de galería
        self.gallery_scroll = QScrollArea()
        self.gallery_scroll.setWidgetResizable(True)
        
        self.gallery_container = QWidget()
        self.gallery_grid = QGridLayout()
        self.gallery_grid.setSpacing(20)
        self.gallery_grid.setContentsMargins(10, 10, 10, 10)
        self.gallery_container.setLayout(self.gallery_grid)
        
        self.gallery_scroll.setWidget(self.gallery_container)
        layout.addWidget(self.gallery_scroll)
        
        # Temporizador para slideshow
        self.slideshow_timer = QTimer()
        self.slideshow_timer.timeout.connect(self.next_slideshow_image)
        self.slideshow_active = False
        self.current_slideshow_index = 0
        
    def setup_about_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        self.about_tab.setLayout(layout)
        
        # Logo
        logo = QLabel()
        logo.setPixmap(QPixmap("gallery.png").scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)
        
        # Título
        title = QLabel("Visual Gallery Explorer Pro")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: var(--primary);
            margin-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Descripción
        desc = QLabel("""
            <p style='font-size: 16px; line-height: 1.5;'>
                Una aplicación moderna para buscar, explorar y descargar imágenes de la web.<br>
                Con interfaz intuitiva y funciones avanzadas para organizar tu colección visual.
            </p>
            <p style='font-size: 14px; color: var(--text-secondary);'>
                <b>Características principales:</b><br>
                • Búsqueda en múltiples motores<br>
                • Filtros avanzados por tamaño y color<br>
                • Galería organizada con slideshow<br>
                • Descarga masiva de imágenes<br>
                • Interfaz oscura personalizable
            </p>
        """)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Créditos
        credits = QLabel("""
            <p style='font-size: 12px; color: var(--text-secondary);'>
                Versión 3.0 | Desarrollado por Jesús | © 2024<br>
                Iconos por Flaticon | Fuentes por Google Fonts
            </p>
        """)
        credits.setAlignment(Qt.AlignCenter)
        layout.addWidget(credits)
        
        layout.addStretch()
        
        # Botones
        btn_layout = QHBoxLayout()
        
        github_btn = QPushButton("⭐ GitHub")
        github_btn.clicked.connect(lambda: webbrowser.open("https://github.com"))
        btn_layout.addWidget(github_btn)
        
        donate_btn = QPushButton("☕ Invitar a un café")
        donate_btn.setObjectName("primary")
        donate_btn.clicked.connect(lambda: webbrowser.open("https://buymeacoffee.com"))
        btn_layout.addWidget(donate_btn)
        
        layout.addLayout(btn_layout)
        
    def search_images(self):
        query = self.search_input.text().strip()
        if not query:
            self.show_status("Por favor, ingresa un término de búsqueda", "error")
            return
            
        self.current_search = query
        self.show_status(f"Buscando imágenes de '{query}'...", "loading")
        QApplication.processEvents()
        
        try:
            # Construir URL de búsqueda según el motor seleccionado
            engine = self.search_type.currentText().lower()
            if engine == "google":
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch"
                headers = {"User-Agent": "Mozilla/5.0"}
            elif engine == "bing":
                url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}"
                headers = {"User-Agent": "Mozilla/5.0"}
            else:  # DuckDuckGo
                url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}&iax=images&ia=images"
                headers = {"User-Agent": "Mozilla/5.0"}
            
            # Añadir parámetros de búsqueda
            if engine == "google":
                # Tamaño
                size_map = {
                    "Grande": "isz:l",
                    "Mediano": "isz:m",
                    "Pequeño": "isz:i"
                }
                size = self.size_combo.currentText()
                if size in size_map:
                    url += f"&tbs={size_map[size]}"
                
                # Color
                color_map = {
                    "Blanco y negro": "ic:gray",
                    "Transparente": "ic:trans",
                    "Rojo": "ic:specific,isc:red",
                    "Azul": "ic:specific,isc:blue",
                    "Verde": "ic:specific,isc:green"
                }
                color = self.color_combo.currentText()
                if color in color_map:
                    url += f",{color_map[color]}" if "tbs=" in url else f"&tbs={color_map[color]}"
                
                # SafeSearch
                if self.safe_search.isChecked():
                    url += "&safe=active"
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer imágenes según el motor de búsqueda
            if engine == "google":
                images = self.parse_google_images(soup)
            elif engine == "bing":
                images = self.parse_bing_images(soup)
            else:  # DuckDuckGo
                images = self.parse_duckduckgo_images(soup)
            
            self.clear_results()
            self.image_urls = []
            self.image_checkboxes = []
            
            # Mostrar imágenes
            for idx, img_url in enumerate(images[:30]):  # Limitar a 30 resultados
                self.add_image_result(img_url, idx)
                self.image_urls.append(img_url)
                self.progress_bar.setValue((idx + 1) * 100 // min(30, len(images)))
                QApplication.processEvents()
            
            self.show_status(f"Se encontraron {len(images)} imágenes para '{query}'", "success")
            
        except Exception as e:
            self.show_status(f"Error al buscar imágenes: {str(e)}", "error")
            
    def parse_google_images(self, soup):
        images = []
        for img in soup.find_all('img'):
            # Saltar el logo de Google
            if 'alt' in img.attrs and img['alt'] == 'Google':
                continue
                
            # Intentar diferentes atributos donde puede estar la URL
            for attr in ['src', 'data-src', 'data-iurl']:
                if attr in img.attrs:
                    img_url = img[attr]
                    if img_url.startswith('http') and not img_url.startswith('https://www.google.com'):
                        images.append(img_url)
                        break
        return images
    
    def parse_bing_images(self, soup):
        images = []
        for img in soup.find_all('img', class_='mimg'):
            if 'src' in img.attrs:
                img_url = img['src']
                if img_url.startswith('http'):
                    images.append(img_url)
        return images
    
    def parse_duckduckgo_images(self, soup):
        images = []
        for img in soup.find_all('img', class_='tile--img__img'):
            if 'data-src' in img.attrs:
                img_url = img['data-src']
                if img_url.startswith('http'):
                    images.append(img_url)
        return images
            
    def add_image_result(self, image_url, index):
        row = index // 4
        col = index % 4
        
        try:
            response = requests.get(image_url, timeout=10)
            img_data = response.content
            
            # Verificar que sea una imagen válida
            if not response.headers.get('content-type', '').startswith('image/'):
                return
                
            pixmap = QPixmap()
            if not pixmap.loadFromData(img_data):
                return
                
            # Crear tarjeta para la imagen
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background: var(--card-bg);
                    border-radius: 8px;
                    border: 1px solid var(--card-border);
                    transition: all 0.2s;
                }
                QFrame:hover {
                    border: 1px solid var(--primary);
                    transform: translateY(-2px);
                }
            """)
            card.setFixedSize(250, 280)
            
            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(10, 10, 10, 10)
            card_layout.setSpacing(10)
            
            # Imagen
            img_label = QLabel()
            img_label.setPixmap(pixmap.scaled(230, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            img_label.setAlignment(Qt.AlignCenter)
            img_label.setStyleSheet("""
                background: transparent;
                border-radius: 4px;
            """)
            img_label.setCursor(QCursor(Qt.PointingHandCursor))
            
            # Checkbox para selección
            checkbox = QCheckBox("Seleccionar")
            checkbox.setCursor(QCursor(Qt.PointingHandCursor))
            
            # Botón de detalles
            details_btn = QPushButton("🔍 Detalles")
            details_btn.setCursor(QCursor(Qt.PointingHandCursor))
            details_btn.setStyleSheet("font-size: 12px; padding: 5px 10px;")
            details_btn.clicked.connect(lambda _, url=image_url, pm=pixmap: self.show_image_details(url, pm))
            
            # Evento para hacer clic en la imagen
            def image_clicked(event, cb=checkbox):
                cb.setChecked(not cb.isChecked())
            img_label.mousePressEvent = image_clicked
            
            card_layout.addWidget(img_label)
            card_layout.addWidget(checkbox)
            card_layout.addWidget(details_btn)
            
            card.setLayout(card_layout)
            self.results_grid.addWidget(card, row, col)
            self.image_checkboxes.append(checkbox)
            
        except Exception as e:
            print(f"Error al cargar imagen: {str(e)}")
            
    def clear_results(self):
        for i in reversed(range(self.results_grid.count())):
            widget = self.results_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.results_container.update()
        self.progress_bar.setValue(0)
                
    def download_selected(self):
        selected_indices = [i for i, cb in enumerate(self.image_checkboxes) if cb.isChecked()]
        if not selected_indices:
            self.show_status("No has seleccionado ninguna imagen para descargar", "warning")
            return
            
        # Crear carpeta de descargas si no existe
        os.makedirs(self.download_folder, exist_ok=True)
        
        # Descargar imágenes
        success_count = 0
        total = len(selected_indices)
        
        for i, idx in enumerate(selected_indices):
            try:
                img_url = self.image_urls[idx]
                response = requests.get(img_url, timeout=10)
                img_data = response.content
                
                # Generar nombre de archivo único
                file_path = os.path.join(self.download_folder, f"{self.current_search}_{i+1}.jpg")
                
                # Guardar imagen
                with open(file_path, 'wb') as f:
                    f.write(img_data)
                
                success_count += 1
                self.progress_bar.setValue((i + 1) * 100 // total)
                QApplication.processEvents()
                
            except Exception as e:
                print(f"Error al descargar imagen: {str(e)}")
                
        if success_count > 0:
            self.show_status(f"Descargadas {success_count} imágenes en '{self.download_folder}'", "success")
            self.load_local_gallery()  # Actualizar galería
        else:
            self.show_status("No se pudo descargar ninguna imagen", "error")
            
    def load_local_gallery(self):
        # Limpiar galería actual
        for i in reversed(range(self.gallery_grid.count())):
            widget = self.gallery_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        # Cargar imágenes de la carpeta local
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder, exist_ok=True)
            
        image_files = [f for f in os.listdir(self.download_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            empty_label = QLabel("No hay imágenes en la galería")
            empty_label.setStyleSheet("font-size: 14px; color: var(--text-secondary);")
            empty_label.setAlignment(Qt.AlignCenter)
            self.gallery_grid.addWidget(empty_label, 0, 0)
            return
            
        for idx, img_file in enumerate(image_files[:30]):  # Mostrar máximo 30 imágenes
            img_path = os.path.join(self.download_folder, img_file)
            try:
                pixmap = QPixmap(img_path)
                if pixmap.isNull():
                    continue
                    
                # Crear tarjeta para la imagen
                card = QFrame()
                card.setStyleSheet("""
                    QFrame {
                        background: var(--card-bg);
                        border-radius: 8px;
                        border: 1px solid var(--card-border);
                    }
                    QFrame:hover {
                        border: 1px solid var(--primary);
                    }
                """)
                card.setFixedSize(220, 250)
                
                card_layout = QVBoxLayout()
                card_layout.setContentsMargins(10, 10, 10, 10)
                card_layout.setSpacing(10)
                
                # Imagen
                img_label = QLabel()
                img_label.setPixmap(pixmap.scaled(200, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                img_label.setAlignment(Qt.AlignCenter)
                img_label.setStyleSheet("background: transparent;")
                img_label.setCursor(QCursor(Qt.PointingHandCursor))
                
                # Nombre del archivo (recortado)
                filename = QLabel(img_file[:15] + "..." if len(img_file) > 15 else img_file)
                filename.setStyleSheet("font-size: 11px; color: var(--text-secondary);")
                filename.setAlignment(Qt.AlignCenter)
                filename.setWordWrap(True)
                
                # Botón de detalles
                details_btn = QPushButton("🔍 Detalles")
                details_btn.setCursor(QCursor(Qt.PointingHandCursor))
                details_btn.setStyleSheet("font-size: 12px; padding: 5px 10px;")
                details_btn.clicked.connect(lambda _, path=img_path, pm=pixmap: self.show_image_details(path, pm))
                
                # Evento para hacer clic en la imagen
                def image_clicked(event, path=img_path, pm=pixmap):
                    self.show_image_details(path, pm)
                img_label.mousePressEvent = image_clicked
                
                card_layout.addWidget(img_label)
                card_layout.addWidget(filename)
                card_layout.addWidget(details_btn)
                
                card.setLayout(card_layout)
                
                row = idx // 4
                col = idx % 4
                self.gallery_grid.addWidget(card, row, col)
                
            except Exception as e:
                print(f"Error al cargar imagen de galería: {str(e)}")
                
        self.show_status(f"Galería actualizada con {len(image_files)} imágenes", "info")
                
    def show_image_details(self, image_source, pixmap):
        dialog = QDialog(self)
        dialog.setWindowTitle("Detalles de la imagen")
        dialog.setMinimumWidth(500)
        dialog.setStyleSheet("""
            QDialog {
                background: var(--bg);
            }
            QLabel {
                color: var(--text);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Imagen
        img_label = QLabel()
        img_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(img_label)
        
        # Metadatos
        meta_layout = QVBoxLayout()
        meta_layout.setSpacing(10)
        
        size_label = QLabel(f"Dimensiones: {pixmap.width()} x {pixmap.height()} px")
        
        source_label = QLabel()
        if image_source.startswith('http'):
            source_label.setText(f"URL: <a href='{image_source}'>{image_source[:50]}...</a>")
            source_label.setOpenExternalLinks(True)
        else:
            source_label.setText(f"Archivo: {os.path.basename(image_source)}")
            
        meta_layout.addWidget(size_label)
        meta_layout.addWidget(source_label)
        layout.addLayout(meta_layout)
        
        # Botones
        btn_box = QDialogButtonBox()
        
        if image_source.startswith('http'):
            copy_btn = QPushButton("📋 Copiar URL")
            copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(image_source))
            btn_box.addButton(copy_btn, QDialogButtonBox.ActionRole)
            
            open_btn = QPushButton("🌐 Abrir en navegador")
            open_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(image_source)))
            btn_box.addButton(open_btn, QDialogButtonBox.ActionRole)
        else:
            open_btn = QPushButton("📂 Mostrar en carpeta")
            open_btn.clicked.connect(lambda: self.open_file_location(image_source))
            btn_box.addButton(open_btn, QDialogButtonBox.ActionRole)
            
        close_btn = btn_box.addButton(QDialogButtonBox.Close)
        close_btn.clicked.connect(dialog.close)
        
        layout.addWidget(btn_box)
        dialog.setLayout(layout)
        dialog.exec_()
        
    def toggle_slideshow(self):
        if self.slideshow_active:
            self.slideshow_timer.stop()
            self.slideshow_btn.setText("🎬 Iniciar slideshow")
            self.slideshow_active = False
        else:
            # Verificar que haya imágenes en la galería
            if self.gallery_grid.count() == 0:
                self.show_status("No hay imágenes para el slideshow", "warning")
                return
                
            self.slideshow_active = True
            self.slideshow_btn.setText("⏹ Detener slideshow")
            self.current_slideshow_index = 0
            speed = 3000 - (self.slideshow_speed.value() * 250)  # 750ms a 3000ms
            self.slideshow_timer.start(speed)
            self.next_slideshow_image()
            
    def next_slideshow_image(self):
        if not self.slideshow_active or self.gallery_grid.count() == 0:
            return
            
        # Ocultar todas las imágenes
        for i in range(self.gallery_grid.count()):
            widget = self.gallery_grid.itemAt(i).widget()
            if widget:
                widget.hide()
                
        # Mostrar la imagen actual
        self.current_slideshow_index = (self.current_slideshow_index + 1) % self.gallery_grid.count()
        widget = self.gallery_grid.itemAt(self.current_slideshow_index).widget()
        if widget:
            widget.show()
            
    def toggle_select_all(self):
        if not self.image_checkboxes:
            return
            
        # Verificar si ya están todos seleccionados
        all_selected = all(cb.isChecked() for cb in self.image_checkboxes)
        
        # Alternar estado
        for checkbox in self.image_checkboxes:
            checkbox.setChecked(not all_selected)
            
        self.select_all.setText("Deseleccionar todo" if not all_selected else "Seleccionar todo")
        
    def open_download_folder(self):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.download_folder))
        
    def open_file_location(self, file_path):
        if sys.platform == "win32":
            os.startfile(os.path.dirname(file_path))
        elif sys.platform == "darwin":
            os.system(f'open "{os.path.dirname(file_path)}"')
        else:
            os.system(f'xdg-open "{os.path.dirname(file_path)}"')
            
    def clear_search(self):
        self.search_input.clear()
        self.clear_results()
        self.show_status("Búsqueda limpiada", "info")
        
    def show_about(self):
        self.tabs.setCurrentIndex(2)  # Cambiar a pestaña "Información"
        
    def show_status(self, message, type="info"):
        colors = {
            "info": "var(--text-secondary)",
            "success": "var(--success)",
            "warning": "var(--warning)",
            "error": "var(--error)",
            "loading": "var(--primary)"
        }
        
        self.status_bar.setText(message)
        self.status_bar.setStyleSheet(f"""
            font-size: 12px;
            color: {colors.get(type, "var(--text-secondary)")};
            padding: 8px;
            border-top: 1px solid var(--card-border);
        """)
        
        # Limpiar mensaje después de 5 segundos (excepto para loading)
        if type != "loading":
            QTimer.singleShot(5000, lambda: self.status_bar.setText("Listo") if self.status_bar.text() == message else None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Establecer estilo general
    app.setStyle("Fusion")
    
    window = ModernImageScraper()
    window.show()
    sys.exit(app.exec_())