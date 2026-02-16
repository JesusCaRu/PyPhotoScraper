"""
Ventana principal de Visual Gallery Explorer Pro.
Interfaz premium con glassmorphism, gradientes y micro-animaciones.
"""
import sys
import os
import webbrowser

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QScrollArea, QGridLayout, QCheckBox, QMessageBox,
    QFrame, QDialog, QDialogButtonBox, QTabWidget, QComboBox,
    QMenuBar, QProgressBar, QSlider, QAction, QApplication,
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
)
from PyQt5.QtGui import (
    QPixmap, QCursor, QDesktopServices, QColor, QPainter,
    QLinearGradient, QFont, QIcon,
)
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize, QPropertyAnimation, QEasingCurve

from ui.styles import (
    GLOBAL_STYLESHEET, ACCENT, ACCENT_LIGHT, ACCENT_GLOW, CYAN, ROSE, AMBER,
    TEXT, TEXT_SECONDARY, TEXT_MUTED, BG, BG_DARK, BG_ELEVATED, BG_DEEPEST,
    SURFACE, SURFACE_LIGHT, SURFACE_HOVER, SURFACE_BORDER,
    STATUS_COLORS, STATUS_ICONS, GRADIENT_ACCENT,
    card_style, status_style, dialog_style, header_style,
    search_card_placeholder_style, gallery_empty_style,
    badge_style, separator_style,
)
from workers.search_worker import SearchWorker
from workers.download_worker import ImageDownloader, ThumbnailLoader


def _shadow(widget, blur=30, offset_y=8, color="#00000060"):
    """Aplica sombra a un widget."""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setOffset(0, offset_y)
    shadow.setColor(QColor(color))
    widget.setGraphicsEffect(shadow)
    return widget


def _make_line():
    """Crea una línea separadora sutil."""
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(separator_style())
    line.setFixedHeight(1)
    return line


class MainWindow(QWidget):
    """Ventana principal premium de la aplicación."""

    IMG_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Gallery Explorer Pro")
        self.resize(1480, 920)

        # ── Estado interno ───────────────────────────────────────────
        self.image_checkboxes: list[QCheckBox] = []
        self.image_urls: list[str] = []
        self._thumb_workers: list[ThumbnailLoader] = []
        self.current_search = ""
        self.download_folder = os.path.join(os.path.dirname(__file__), "..", "Imagenes")
        self.download_folder = os.path.abspath(self.download_folder)

        # ── Estilo ───────────────────────────────────────────────────
        self.setStyleSheet(GLOBAL_STYLESHEET)

        # ── Interfaz ─────────────────────────────────────────────────
        self._build_ui()

        # Cargar galería tras un pequeño delay
        QTimer.singleShot(300, self.load_local_gallery)

    # ═════════════════════════════════════════════════════════════════
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ═════════════════════════════════════════════════════════════════

    def _build_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self.setLayout(root)

        # Menú
        self._build_menu_bar(root)

        # Header banner
        self._build_header(root)

        # Contenido principal
        content = QVBoxLayout()
        content.setContentsMargins(24, 8, 24, 0)
        content.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.search_tab = QWidget()
        self._build_search_tab()
        self.tabs.addTab(self.search_tab, "🔍  Buscador")

        self.gallery_tab = QWidget()
        self._build_gallery_tab()
        self.tabs.addTab(self.gallery_tab, "🖼  Galería")

        self.about_tab = QWidget()
        self._build_about_tab()
        self.tabs.addTab(self.about_tab, "✨  Acerca de")

        content.addWidget(self.tabs)
        root.addLayout(content)

        # Status bar
        self.status_bar = QLabel("💡 Listo para buscar")
        self.status_bar.setStyleSheet(status_style(TEXT_SECONDARY))
        root.addWidget(self.status_bar)

    # ── Header ───────────────────────────────────────────────────────
    def _build_header(self, parent):
        header = QFrame()
        header.setFixedHeight(72)
        header.setStyleSheet(header_style())

        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(28, 0, 28, 0)

        # Logo text con gradiente
        logo = QLabel("⚡")
        logo.setStyleSheet(f"font-size: 28px; background: transparent;")

        title = QLabel("Visual Gallery Explorer")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 800;
            color: {TEXT};
            background: transparent;
            letter-spacing: 0.5px;
        """)

        pro_badge = QLabel("PRO")
        pro_badge.setStyleSheet(f"""
            background: {ACCENT};
            color: white;
            border-radius: 8px;
            padding: 3px 10px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
        """)

        h_layout.addWidget(logo)
        h_layout.addWidget(title)
        h_layout.addWidget(pro_badge)
        h_layout.addStretch()

        # Contador de imágenes en galería
        self.gallery_counter = QLabel("0 imágenes")
        self.gallery_counter.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 12px;
            font-weight: 600;
            background: transparent;
            padding-right: 8px;
        """)
        h_layout.addWidget(self.gallery_counter)

        parent.addWidget(header)

    # ── Menú ─────────────────────────────────────────────────────────
    def _build_menu_bar(self, parent):
        menubar = QMenuBar()

        file_menu = menubar.addMenu("  Archivo  ")
        self._add_action(file_menu, "🔍  Nueva búsqueda", self.clear_search)
        self._add_action(file_menu, "📂  Abrir carpeta de descargas", self.open_download_folder)
        file_menu.addSeparator()
        self._add_action(file_menu, "🚪  Salir", self.close)

        help_menu = menubar.addMenu("  Ayuda  ")
        self._add_action(help_menu, "✨  Acerca de", lambda: self.tabs.setCurrentIndex(2))

        parent.addWidget(menubar)

    @staticmethod
    def _add_action(menu, text, slot):
        action = QAction(text, menu)
        action.triggered.connect(slot)
        menu.addAction(action)

    # ══════════════════════════════════════════════════════════════════
    #  PESTAÑA DE BÚSQUEDA
    # ══════════════════════════════════════════════════════════════════

    def _build_search_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(16)
        self.search_tab.setLayout(layout)

        # ── Panel de búsqueda (glass card) ───────────────────────────
        search_panel = QFrame()
        search_panel.setStyleSheet(f"""
            QFrame {{
                background: {BG_ELEVATED};
                border-radius: 18px;
                border: 1px solid {SURFACE_BORDER};
            }}
        """)

        sp_layout = QVBoxLayout(search_panel)
        sp_layout.setContentsMargins(24, 20, 24, 20)
        sp_layout.setSpacing(16)

        # Título del panel
        panel_header = QHBoxLayout()
        panel_title = QLabel("🔍  Buscar imágenes")
        panel_title.setStyleSheet(f"""
            font-size: 16px; font-weight: 700; color: {TEXT};
            background: transparent;
        """)
        panel_header.addWidget(panel_title)
        panel_header.addStretch()
        sp_layout.addLayout(panel_header)

        # Fila de búsqueda
        search_row = QHBoxLayout()
        search_row.setSpacing(12)

        self.search_type = QComboBox()
        self.search_type.addItems(["Google", "Bing", "DuckDuckGo"])
        self.search_type.setMinimumHeight(48)
        search_row.addWidget(self.search_type)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Escribe qué imágenes quieres encontrar...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setMinimumHeight(48)
        self.search_input.returnPressed.connect(self.search_images)
        search_row.addWidget(self.search_input, 1)

        self.search_btn = QPushButton("🚀  Buscar")
        self.search_btn.setObjectName("primary")
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_btn.setMinimumHeight(48)
        self.search_btn.setMinimumWidth(140)
        self.search_btn.clicked.connect(self.search_images)
        search_row.addWidget(self.search_btn)

        sp_layout.addLayout(search_row)

        # Filtros
        sp_layout.addWidget(_make_line())

        filters = QHBoxLayout()
        filters.setSpacing(12)

        filters.addWidget(self._filter_label("📐 Tamaño"))
        self.size_combo = QComboBox()
        self.size_combo.addItems(["Cualquier tamaño", "Grande", "Mediano", "Pequeño"])
        filters.addWidget(self.size_combo)

        filters.addWidget(self._filter_label("🎨 Color"))
        self.color_combo = QComboBox()
        self.color_combo.addItems([
            "Cualquier color", "Blanco y negro", "Transparente",
            "Rojo", "Azul", "Verde",
        ])
        filters.addWidget(self.color_combo)

        self.safe_search = QCheckBox("🛡️ SafeSearch")
        self.safe_search.setChecked(True)
        self.safe_search.setStyleSheet(f"font-weight: 600; background: transparent;")
        filters.addWidget(self.safe_search)

        filters.addStretch()
        sp_layout.addLayout(filters)

        layout.addWidget(search_panel)

        # ── Panel de resultados ──────────────────────────────────────
        results_panel = QFrame()
        results_panel.setStyleSheet(f"""
            QFrame {{
                background: {BG_ELEVATED};
                border-radius: 18px;
                border: 1px solid {SURFACE_BORDER};
            }}
        """)

        rp_layout = QVBoxLayout(results_panel)
        rp_layout.setContentsMargins(24, 16, 24, 16)
        rp_layout.setSpacing(12)

        # Header de resultados
        results_header = QHBoxLayout()
        results_title = QLabel("📷  Resultados")
        results_title.setStyleSheet(f"""
            font-size: 16px; font-weight: 700; color: {TEXT};
            background: transparent;
        """)
        results_header.addWidget(results_title)

        self.results_count = QLabel("")
        self.results_count.setStyleSheet(badge_style(ACCENT))
        self.results_count.hide()
        results_header.addWidget(self.results_count)

        results_header.addStretch()

        self.select_all_btn = QPushButton("☑  Seleccionar todo")
        self.select_all_btn.setObjectName("ghost")
        self.select_all_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        results_header.addWidget(self.select_all_btn)

        self.download_btn = QPushButton("📥  Descargar")
        self.download_btn.setObjectName("accent")
        self.download_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.download_btn.clicked.connect(self.download_selected)
        results_header.addWidget(self.download_btn)

        rp_layout.addLayout(results_header)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.hide()
        rp_layout.addWidget(self.progress_bar)

        # Grid de resultados
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_container.setStyleSheet("background: transparent;")
        self.results_grid = QGridLayout()
        self.results_grid.setSpacing(16)
        self.results_grid.setContentsMargins(0, 8, 0, 8)
        self.results_container.setLayout(self.results_grid)
        self.scroll_area.setWidget(self.results_container)
        rp_layout.addWidget(self.scroll_area)

        layout.addWidget(results_panel)

    @staticmethod
    def _filter_label(text):
        lbl = QLabel(text)
        lbl.setStyleSheet(f"""
            font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY};
            background: transparent;
        """)
        return lbl

    # ══════════════════════════════════════════════════════════════════
    #  PESTAÑA DE GALERÍA
    # ══════════════════════════════════════════════════════════════════

    def _build_gallery_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(16)
        self.gallery_tab.setLayout(layout)

        # Barra de herramientas
        toolbar = QFrame()
        toolbar.setStyleSheet(f"""
            QFrame {{
                background: {BG_ELEVATED};
                border-radius: 14px;
                border: 1px solid {SURFACE_BORDER};
            }}
        """)
        toolbar.setFixedHeight(60)

        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(20, 0, 20, 0)
        tb_layout.setSpacing(10)

        self.refresh_btn = QPushButton("🔄  Actualizar")
        self.refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_btn.clicked.connect(self.load_local_gallery)
        tb_layout.addWidget(self.refresh_btn)

        self.slideshow_btn = QPushButton("▶  Slideshow")
        self.slideshow_btn.setObjectName("accent")
        self.slideshow_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.slideshow_btn.clicked.connect(self.toggle_slideshow)
        tb_layout.addWidget(self.slideshow_btn)

        # Separador visual
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet(f"background: {SURFACE_BORDER}; max-width: 1px;")
        tb_layout.addWidget(sep)

        speed_label = QLabel("⚡ Velocidad")
        speed_label.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {TEXT_SECONDARY}; background: transparent;")
        tb_layout.addWidget(speed_label)

        self.slideshow_speed = QSlider(Qt.Horizontal)
        self.slideshow_speed.setRange(1, 10)
        self.slideshow_speed.setValue(4)
        self.slideshow_speed.setMaximumWidth(120)
        tb_layout.addWidget(self.slideshow_speed)

        tb_layout.addStretch()

        self.gallery_badge = QLabel("0")
        self.gallery_badge.setStyleSheet(badge_style(ACCENT))
        tb_layout.addWidget(self.gallery_badge)

        self.clear_gallery_btn = QPushButton("🗑  Limpiar")
        self.clear_gallery_btn.setObjectName("danger")
        self.clear_gallery_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.clear_gallery_btn.clicked.connect(self.clear_local_gallery)
        tb_layout.addWidget(self.clear_gallery_btn)

        layout.addWidget(toolbar)

        # Grid de galería
        self.gallery_scroll = QScrollArea()
        self.gallery_scroll.setWidgetResizable(True)
        self.gallery_container = QWidget()
        self.gallery_container.setStyleSheet("background: transparent;")
        self.gallery_grid = QGridLayout()
        self.gallery_grid.setSpacing(16)
        self.gallery_grid.setContentsMargins(4, 8, 4, 8)
        self.gallery_container.setLayout(self.gallery_grid)
        self.gallery_scroll.setWidget(self.gallery_container)
        layout.addWidget(self.gallery_scroll)

        # Slideshow timer
        self.slideshow_timer = QTimer()
        self.slideshow_timer.timeout.connect(self._next_slideshow_image)
        self.slideshow_active = False
        self.current_slideshow_index = 0

    # ══════════════════════════════════════════════════════════════════
    #  PESTAÑA ACERCA DE
    # ══════════════════════════════════════════════════════════════════

    def _build_about_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 30, 0, 30)
        layout.setSpacing(0)
        self.about_tab.setLayout(layout)

        layout.addStretch(2)

        # Card principal
        about_card = QFrame()
        about_card.setMaximumWidth(600)
        about_card.setStyleSheet(f"""
            QFrame {{
                background: {BG_ELEVATED};
                border-radius: 24px;
                border: 1px solid {SURFACE_BORDER};
            }}
        """)

        card_layout = QVBoxLayout(about_card)
        card_layout.setContentsMargins(40, 36, 40, 36)
        card_layout.setSpacing(16)

        # Icono animado
        icon_label = QLabel("⚡")
        icon_label.setStyleSheet("font-size: 48px; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)

        title = QLabel("Visual Gallery Explorer")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 800;
            color: {TEXT};
            background: transparent;
            letter-spacing: -0.5px;
        """)
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Busca, explora y descarga imágenes con estilo")
        subtitle.setStyleSheet(f"""
            font-size: 14px; color: {TEXT_SECONDARY};
            background: transparent; margin-bottom: 8px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addWidget(_make_line())

        # Features grid
        features = [
            ("🔍", "Multi-motor", "Google, Bing & DuckDuckGo"),
            ("🎨", "Filtros avanzados", "Tamaño, color y SafeSearch"),
            ("📥", "Descarga masiva", "Múltiples imágenes a la vez"),
            ("🖼", "Galería inteligente", "Slideshow y organización"),
        ]

        features_grid = QGridLayout()
        features_grid.setSpacing(12)
        for i, (icon, name, desc) in enumerate(features):
            feat = QFrame()
            feat.setStyleSheet(f"""
                QFrame {{
                    background: {SURFACE};
                    border-radius: 12px;
                    border: 1px solid {SURFACE_BORDER};
                }}
            """)
            fl = QVBoxLayout(feat)
            fl.setContentsMargins(14, 12, 14, 12)
            fl.setSpacing(4)

            fi = QLabel(f"{icon}  {name}")
            fi.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {TEXT}; background: transparent;")
            fl.addWidget(fi)

            fd = QLabel(desc)
            fd.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
            fl.addWidget(fd)

            features_grid.addWidget(feat, i // 2, i % 2)

        card_layout.addLayout(features_grid)

        card_layout.addWidget(_make_line())

        version = QLabel("v5.0  ·  Desarrollado por Jesús  ·  2024")
        version.setStyleSheet(f"font-size: 11px; color: {TEXT_MUTED}; background: transparent;")
        version.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(version)

        # Botones
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        github_btn = QPushButton("⭐  GitHub")
        github_btn.setObjectName("ghost")
        github_btn.setCursor(QCursor(Qt.PointingHandCursor))
        github_btn.clicked.connect(lambda: webbrowser.open("https://github.com"))
        btn_row.addWidget(github_btn)

        donate_btn = QPushButton("☕  Invitar a un café")
        donate_btn.setObjectName("primary")
        donate_btn.setCursor(QCursor(Qt.PointingHandCursor))
        donate_btn.clicked.connect(lambda: webbrowser.open("https://buymeacoffee.com"))
        btn_row.addWidget(donate_btn)

        card_layout.addLayout(btn_row)

        # Centrar la card
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(about_card)
        center_layout.addStretch()
        layout.addLayout(center_layout)

        layout.addStretch(3)

    # ═════════════════════════════════════════════════════════════════
    #  BÚSQUEDA
    # ═════════════════════════════════════════════════════════════════

    def search_images(self):
        query = self.search_input.text().strip()
        if not query:
            self._show_status("Escribe qué quieres buscar primero", "warning")
            return

        self.current_search = query
        self._show_status(f"Buscando «{query}»...", "loading")
        self.search_btn.setEnabled(False)
        self.search_btn.setText("⏳  Buscando...")
        self.progress_bar.setValue(0)
        self.progress_bar.show()

        options = {
            "size": self.size_combo.currentText(),
            "color": self.color_combo.currentText(),
            "safe": self.safe_search.isChecked(),
        }
        engine = self.search_type.currentText().lower()

        self._search_worker = SearchWorker(query, engine, options)
        self._search_worker.finished.connect(self._on_search_done)
        self._search_worker.error.connect(self._on_search_error)
        self._search_worker.start()

    def _on_search_done(self, images: list[str]):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("🚀  Buscar")
        self._clear_results()
        self.image_urls = []
        self.image_checkboxes = []

        if not images:
            self._show_status("No se encontraron resultados. Prueba otra búsqueda.", "warning")
            self.results_count.hide()
            self.progress_bar.hide()
            return

        total = len(images)
        for idx, url in enumerate(images):
            self._add_image_card(url, idx)
            self.image_urls.append(url)
            self.progress_bar.setValue((idx + 1) * 100 // total)

        # Actualizar badge de resultados
        self.results_count.setText(f"  {total}  ")
        self.results_count.show()

        display = self.current_search
        if len(display) > 25:
            display = display[:22] + "..."
        self._show_status(f"{total} imágenes encontradas para «{display}»", "success")

        QTimer.singleShot(500, lambda: self.progress_bar.hide())

    def _on_search_error(self, msg: str):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("🚀  Buscar")
        self.progress_bar.hide()
        self._show_status(f"Error en la búsqueda: {msg}", "error")

    # ═════════════════════════════════════════════════════════════════
    #  TARJETAS DE RESULTADOS
    # ═════════════════════════════════════════════════════════════════

    def _add_image_card(self, image_url: str, index: int):
        """Crea una tarjeta premium con placeholder y carga la miniatura."""
        row, col = divmod(index, 4)

        card = QFrame()
        card.setStyleSheet(card_style())
        card.setFixedSize(260, 300)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(10)

        # Contenedor de imagen con fondo oscuro
        img_container = QFrame()
        img_container.setFixedSize(236, 200)
        img_container.setStyleSheet(f"""
            QFrame {{
                background: {SURFACE};
                border-radius: 12px;
                border: none;
            }}
        """)
        img_inner = QVBoxLayout(img_container)
        img_inner.setContentsMargins(0, 0, 0, 0)

        img_label = QLabel("⏳")
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setFixedSize(236, 200)
        img_label.setStyleSheet(search_card_placeholder_style())
        img_inner.addWidget(img_label)

        # Fila inferior: checkbox + botón
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(8)

        checkbox = QCheckBox("Seleccionar")
        checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        checkbox.setStyleSheet(f"font-size: 12px; background: transparent;")

        details_btn = QPushButton("🔍 Ver")
        details_btn.setCursor(QCursor(Qt.PointingHandCursor))
        details_btn.setEnabled(False)
        details_btn.setFixedWidth(80)
        details_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 12px; padding: 6px 10px;
                min-width: 60px; border-radius: 8px;
                background: {SURFACE}; color: {TEXT_SECONDARY};
                border: 1px solid {SURFACE_BORDER};
            }}
            QPushButton:hover {{
                background: {SURFACE_HOVER}; color: {TEXT};
                border: 1px solid {ACCENT};
            }}
            QPushButton:disabled {{
                color: {TEXT_MUTED}; background: {BG_ELEVATED};
                border: 1px solid {BG_ELEVATED};
            }}
        """)

        bottom_row.addWidget(checkbox)
        bottom_row.addStretch()
        bottom_row.addWidget(details_btn)

        # Clic en imagen alterna el checkbox
        img_label.setCursor(QCursor(Qt.PointingHandCursor))
        img_label.mousePressEvent = lambda ev, cb=checkbox: cb.setChecked(not cb.isChecked())

        card_layout.addWidget(img_container)
        card_layout.addLayout(bottom_row)
        card.setLayout(card_layout)

        self.results_grid.addWidget(card, row, col)
        self.image_checkboxes.append(checkbox)

        # Cargar thumbnail en hilo (emite bytes, NO QPixmap)
        worker = ThumbnailLoader(image_url, index)
        worker.loaded.connect(
            lambda data, idx, lbl=img_label, btn=details_btn, url=image_url:
                self._on_thumb_loaded(data, lbl, btn, url)
        )
        worker.failed.connect(
            lambda idx, lbl=img_label: self._on_thumb_failed(lbl)
        )
        worker.start()
        self._thumb_workers.append(worker)

    def _on_thumb_loaded(self, data: bytes, label: QLabel, button: QPushButton, url: str):
        """Slot en el hilo principal: crea QPixmap de los bytes recibidos."""
        pixmap = QPixmap()
        if pixmap.loadFromData(data):
            label.setText("")
            label.setStyleSheet(f"background: transparent; border-radius: 12px;")
            label.setPixmap(pixmap.scaled(236, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            button.setEnabled(True)
            button.clicked.connect(lambda: self._show_image_details(url, pixmap))

    def _on_thumb_failed(self, label: QLabel):
        label.setText("✕")
        label.setStyleSheet(f"""
            background: {BG_DARK}; border-radius: 12px;
            color: {TEXT_MUTED}; font-size: 24px;
        """)

    def _clear_results(self):
        for w in self._thumb_workers:
            if w.isRunning():
                w.quit()
                w.wait(500)
        self._thumb_workers.clear()

        for i in reversed(range(self.results_grid.count())):
            widget = self.results_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.progress_bar.setValue(0)

    # ═════════════════════════════════════════════════════════════════
    #  DESCARGA
    # ═════════════════════════════════════════════════════════════════

    def download_selected(self):
        selected = [
            self.image_urls[i]
            for i, cb in enumerate(self.image_checkboxes)
            if cb.isChecked()
        ]
        if not selected:
            self._show_status("Selecciona al menos una imagen para descargar", "warning")
            return

        self._show_status(f"Descargando {len(selected)} imágenes...", "loading")
        self.download_btn.setEnabled(False)
        self.download_btn.setText("⏳  Descargando...")
        self.progress_bar.setValue(0)
        self.progress_bar.show()

        prefix = self.current_search.replace(" ", "_")[:30]
        self._dl_worker = ImageDownloader(selected, self.download_folder, prefix)
        self._dl_worker.progress.connect(
            lambda cur, tot: self.progress_bar.setValue(cur * 100 // tot)
        )
        self._dl_worker.finished.connect(self._on_download_done)
        self._dl_worker.start()

    def _on_download_done(self, count: int):
        self.download_btn.setEnabled(True)
        self.download_btn.setText("📥  Descargar")
        self.progress_bar.hide()
        if count > 0:
            self._show_status(f"{count} imágenes descargadas correctamente", "success")
            self.load_local_gallery()
        else:
            self._show_status("No se pudo descargar ninguna imagen", "error")

    # ═════════════════════════════════════════════════════════════════
    #  GALERÍA LOCAL
    # ═════════════════════════════════════════════════════════════════

    def _get_gallery_files(self) -> list[str]:
        os.makedirs(self.download_folder, exist_ok=True)
        return sorted([
            f for f in os.listdir(self.download_folder)
            if f.lower().endswith(self.IMG_EXTENSIONS)
        ])

    def load_local_gallery(self):
        """Carga las imágenes descargadas en la galería."""
        for i in reversed(range(self.gallery_grid.count())):
            w = self.gallery_grid.itemAt(i).widget()
            if w:
                w.deleteLater()

        image_files = self._get_gallery_files()
        count = len(image_files)

        # Actualizar contadores
        self.gallery_badge.setText(f"  {count}  ")
        self.gallery_counter.setText(f"📷 {count} imágenes")

        if not image_files:
            empty_widget = QFrame()
            empty_widget.setStyleSheet(f"""
                QFrame {{
                    background: {BG_ELEVATED};
                    border-radius: 20px;
                    border: 2px dashed {SURFACE_BORDER};
                }}
            """)
            empty_widget.setMinimumHeight(300)
            el = QVBoxLayout(empty_widget)
            el.setAlignment(Qt.AlignCenter)

            icon = QLabel("🖼")
            icon.setStyleSheet("font-size: 48px; background: transparent;")
            icon.setAlignment(Qt.AlignCenter)
            el.addWidget(icon)

            msg = QLabel("Tu galería está vacía")
            msg.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {TEXT}; background: transparent;")
            msg.setAlignment(Qt.AlignCenter)
            el.addWidget(msg)

            hint = QLabel("Busca y descarga imágenes para empezar tu colección")
            hint.setStyleSheet(f"font-size: 13px; color: {TEXT_MUTED}; background: transparent;")
            hint.setAlignment(Qt.AlignCenter)
            el.addWidget(hint)

            self.gallery_grid.addWidget(empty_widget, 0, 0, 1, 4)
            return

        for idx, filename in enumerate(image_files[:60]):
            img_path = os.path.join(self.download_folder, filename)
            try:
                pixmap = QPixmap(img_path)
                if pixmap.isNull():
                    continue

                card = QFrame()
                card.setStyleSheet(card_style())
                card.setFixedSize(240, 280)

                cl = QVBoxLayout()
                cl.setContentsMargins(12, 12, 12, 12)
                cl.setSpacing(8)

                # Container de imagen
                img_container = QFrame()
                img_container.setFixedSize(216, 190)
                img_container.setStyleSheet(f"""
                    QFrame {{
                        background: {SURFACE};
                        border-radius: 12px;
                        border: none;
                    }}
                """)
                ic_layout = QVBoxLayout(img_container)
                ic_layout.setContentsMargins(0, 0, 0, 0)

                img_label = QLabel()
                img_label.setPixmap(pixmap.scaled(216, 190, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                img_label.setAlignment(Qt.AlignCenter)
                img_label.setStyleSheet("background: transparent;")
                img_label.setCursor(QCursor(Qt.PointingHandCursor))
                ic_layout.addWidget(img_label)

                # Información del archivo
                short = filename if len(filename) <= 22 else filename[:19] + "..."
                name_label = QLabel(short)
                name_label.setStyleSheet(f"""
                    font-size: 11px; color: {TEXT_SECONDARY};
                    background: transparent; font-weight: 500;
                """)
                name_label.setAlignment(Qt.AlignLeft)

                # Tamaño del archivo
                try:
                    file_size = os.path.getsize(img_path)
                    if file_size > 1_000_000:
                        size_text = f"{file_size / 1_000_000:.1f} MB"
                    else:
                        size_text = f"{file_size / 1000:.0f} KB"
                except Exception:
                    size_text = ""

                info_row = QHBoxLayout()
                info_row.addWidget(name_label)
                if size_text:
                    size_label = QLabel(size_text)
                    size_label.setStyleSheet(f"font-size: 10px; color: {TEXT_MUTED}; background: transparent;")
                    info_row.addStretch()
                    info_row.addWidget(size_label)

                img_label.mousePressEvent = (
                    lambda ev, p=img_path, pm=pixmap: self._show_image_details(p, pm)
                )

                cl.addWidget(img_container)
                cl.addLayout(info_row)
                card.setLayout(cl)

                row, col = divmod(idx, 4)
                self.gallery_grid.addWidget(card, row, col)

            except Exception as e:
                print(f"[Gallery] Error cargando {filename}: {e}")

        self._show_status(f"Galería actualizada · {count} imágenes", "info")

    def clear_local_gallery(self):
        reply = QMessageBox.question(
            self, "Limpiar Galería",
            "¿Eliminar todas las imágenes descargadas?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            try:
                for f in os.listdir(self.download_folder):
                    if f.lower().endswith(self.IMG_EXTENSIONS):
                        os.remove(os.path.join(self.download_folder, f))
                self.load_local_gallery()
                self._show_status("Galería limpiada", "success")
            except Exception as e:
                self._show_status(f"Error: {e}", "error")

    # ═════════════════════════════════════════════════════════════════
    #  DETALLES DE IMAGEN
    # ═════════════════════════════════════════════════════════════════

    def _show_image_details(self, source: str, pixmap: QPixmap):
        dialog = QDialog(self)
        dialog.setWindowTitle("Detalles de la imagen")
        dialog.setMinimumSize(650, 500)
        dialog.setStyleSheet(dialog_style())

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Imagen con fondo
        img_frame = QFrame()
        img_frame.setStyleSheet(f"""
            QFrame {{
                background: {SURFACE};
                border-radius: 16px;
                border: 1px solid {SURFACE_BORDER};
            }}
        """)
        if_layout = QVBoxLayout(img_frame)
        if_layout.setContentsMargins(16, 16, 16, 16)

        img_label = QLabel()
        img_label.setPixmap(pixmap.scaled(560, 420, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setStyleSheet("background: transparent;")
        if_layout.addWidget(img_label)
        layout.addWidget(img_frame)

        # Metadatos
        meta_frame = QFrame()
        meta_frame.setStyleSheet(f"""
            QFrame {{
                background: {BG_ELEVATED};
                border-radius: 12px;
                border: 1px solid {SURFACE_BORDER};
            }}
        """)
        ml = QVBoxLayout(meta_frame)
        ml.setContentsMargins(16, 12, 16, 12)
        ml.setSpacing(6)

        size_lbl = QLabel(f"📐  {pixmap.width()} × {pixmap.height()} px")
        size_lbl.setStyleSheet(f"font-size: 13px; color: {TEXT}; background: transparent; font-weight: 600;")
        ml.addWidget(size_lbl)

        if source.startswith("http"):
            short_url = source[:80] + ("..." if len(source) > 80 else "")
            src_lbl = QLabel(f"🔗  <a href='{source}' style='color: {ACCENT};'>{short_url}</a>")
            src_lbl.setOpenExternalLinks(True)
            src_lbl.setStyleSheet(f"font-size: 12px; background: transparent;")
        else:
            src_lbl = QLabel(f"📁  {os.path.basename(source)}")
            src_lbl.setStyleSheet(f"font-size: 13px; color: {TEXT}; background: transparent;")
        ml.addWidget(src_lbl)
        layout.addWidget(meta_frame)

        # Botones
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        if source.startswith("http"):
            copy_btn = QPushButton("📋  Copiar URL")
            copy_btn.setCursor(QCursor(Qt.PointingHandCursor))
            copy_btn.clicked.connect(lambda: (
                QApplication.clipboard().setText(source),
                self._show_status("URL copiada al portapapeles", "success"),
            ))
            btn_row.addWidget(copy_btn)

            open_btn = QPushButton("🌐  Abrir")
            open_btn.setObjectName("accent")
            open_btn.setCursor(QCursor(Qt.PointingHandCursor))
            open_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(source)))
            btn_row.addWidget(open_btn)
        else:
            open_btn = QPushButton("📂  Abrir carpeta")
            open_btn.setCursor(QCursor(Qt.PointingHandCursor))
            open_btn.clicked.connect(lambda: self._open_file_location(source))
            btn_row.addWidget(open_btn)

        btn_row.addStretch()

        close_btn = QPushButton("Cerrar")
        close_btn.setObjectName("ghost")
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.clicked.connect(dialog.close)
        btn_row.addWidget(close_btn)

        layout.addLayout(btn_row)
        dialog.setLayout(layout)
        dialog.exec_()

    # ═════════════════════════════════════════════════════════════════
    #  SLIDESHOW
    # ═════════════════════════════════════════════════════════════════

    def toggle_slideshow(self):
        if self.slideshow_active:
            self._stop_slideshow()
        else:
            files = self._get_gallery_files()
            if not files:
                self._show_status("No hay imágenes para el slideshow", "warning")
                return

            self.slideshow_active = True
            self.slideshow_btn.setText("⏹  Detener")
            self.slideshow_btn.setObjectName("danger")
            self.slideshow_btn.setStyle(self.slideshow_btn.style())  # force re-style
            self.current_slideshow_index = -1

            speed = max(500, 3500 - self.slideshow_speed.value() * 300)
            self.slideshow_timer.start(speed)
            self._next_slideshow_image()

    def _stop_slideshow(self):
        self.slideshow_timer.stop()
        self.slideshow_btn.setText("▶  Slideshow")
        self.slideshow_btn.setObjectName("accent")
        self.slideshow_btn.setStyle(self.slideshow_btn.style())
        self.slideshow_active = False
        if hasattr(self, "_ss_dialog") and self._ss_dialog.isVisible():
            self._ss_dialog.close()

    def _next_slideshow_image(self):
        if not self.slideshow_active:
            return

        files = self._get_gallery_files()
        if not files:
            self._stop_slideshow()
            return

        self.current_slideshow_index = (self.current_slideshow_index + 1) % len(files)
        path = os.path.join(self.download_folder, files[self.current_slideshow_index])
        pixmap = QPixmap(path)
        if pixmap.isNull():
            return

        if not hasattr(self, "_ss_dialog") or not self._ss_dialog.isVisible():
            self._ss_dialog = QDialog(self, Qt.FramelessWindowHint)
            self._ss_dialog.setStyleSheet(f"background: {BG_DEEPEST};")
            self._ss_dialog.showFullScreen()

            ss_root = QVBoxLayout(self._ss_dialog)
            ss_root.setContentsMargins(0, 0, 0, 0)

            # Top bar con controles
            top = QHBoxLayout()
            top.setContentsMargins(20, 12, 20, 0)

            counter = QLabel(f"{self.current_slideshow_index + 1} / {len(files)}")
            counter.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px; font-weight: 600;")
            top.addWidget(counter)
            self._ss_counter = counter

            top.addStretch()

            close_x = QPushButton("✕")
            close_x.setStyleSheet(f"""
                font-size: 22px; color: {TEXT_SECONDARY};
                background: transparent; border: none;
                padding: 8px 14px; min-width: 40px;
            """)
            close_x.setCursor(QCursor(Qt.PointingHandCursor))
            close_x.clicked.connect(self._stop_slideshow)
            top.addWidget(close_x)

            ss_root.addLayout(top)

            self._ss_label = QLabel()
            self._ss_label.setAlignment(Qt.AlignCenter)
            self._ss_label.setStyleSheet("background: transparent;")
            ss_root.addWidget(self._ss_label, 1)

            # Hint inferior
            hint = QLabel("Pulsa ESC o haz clic para salir")
            hint.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; padding: 8px;")
            hint.setAlignment(Qt.AlignCenter)
            ss_root.addWidget(hint)

            self._ss_dialog.keyPressEvent = lambda e: (
                self._stop_slideshow() if e.key() == Qt.Key_Escape else None
            )
            self._ss_dialog.mousePressEvent = lambda e: self._stop_slideshow()

        # Actualizar imagen y contador
        screen = self._ss_dialog.size()
        margin = QSize(screen.width() - 80, screen.height() - 120)
        self._ss_label.setPixmap(
            pixmap.scaled(margin, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        files = self._get_gallery_files()
        self._ss_counter.setText(f"{self.current_slideshow_index + 1} / {len(files)}")

    # ═════════════════════════════════════════════════════════════════
    #  UTILIDADES
    # ═════════════════════════════════════════════════════════════════

    def toggle_select_all(self):
        if not self.image_checkboxes:
            return
        all_checked = all(cb.isChecked() for cb in self.image_checkboxes)
        for cb in self.image_checkboxes:
            cb.setChecked(not all_checked)
        self.select_all_btn.setText(
            "☐  Deseleccionar" if not all_checked else "☑  Seleccionar todo"
        )

    def open_download_folder(self):
        os.makedirs(self.download_folder, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.download_folder))

    def _open_file_location(self, file_path: str):
        folder = os.path.dirname(file_path)
        if sys.platform == "win32":
            os.startfile(folder)
        elif sys.platform == "darwin":
            os.system(f'open "{folder}"')
        else:
            os.system(f'xdg-open "{folder}"')

    def clear_search(self):
        self.search_input.clear()
        self._clear_results()
        self.image_urls.clear()
        self.image_checkboxes.clear()
        self.results_count.hide()
        self._show_status("Búsqueda limpiada", "info")

    def _show_status(self, message: str, msg_type: str = "info"):
        icon = STATUS_ICONS.get(msg_type, "💡")
        color = STATUS_COLORS.get(msg_type, TEXT_SECONDARY)
        self.status_bar.setText(f"{icon}  {message}")
        self.status_bar.setStyleSheet(status_style(color))

        if msg_type != "loading":
            QTimer.singleShot(
                6000,
                lambda: (
                    self.status_bar.setText("💡 Listo")
                    if self.status_bar.text() == f"{icon}  {message}"
                    else None
                ),
            )
