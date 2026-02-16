"""
Constantes de estilo y tema premium de la aplicación.
Tema oscuro con acentos gradient, glassmorphism y micro-interacciones.
"""

# ─── Paleta de colores ───────────────────────────────────────────────
# Fondo
BG_DEEPEST = "#0d1017"
BG_DARK = "#141820"
BG = "#1a1f2e"
BG_ELEVATED = "#1e2435"

# Superficies
SURFACE = "#232a3b"
SURFACE_LIGHT = "#2a3348"
SURFACE_HOVER = "#303a52"
SURFACE_BORDER = "#2f3a50"

# Acentos
ACCENT = "#6c63ff"         # Violeta principal
ACCENT_LIGHT = "#8b83ff"   # Violeta claro
ACCENT_GLOW = "#6c63ff40"  # Violeta con transparencia
CYAN = "#00d4aa"           # Cian para éxito
CYAN_DARK = "#00b892"
AMBER = "#ffb347"          # Ámbar para warnings
ROSE = "#ff6b6b"           # Rosa para errores
BLUE = "#4dabf7"           # Azul info

# Texto
TEXT = "#e8eaf0"
TEXT_SECONDARY = "#8892a8"
TEXT_MUTED = "#5a6478"

# Gradientes (como strings para uso en QSS)
GRADIENT_ACCENT = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6c63ff, stop:1 #00d4aa)"
GRADIENT_HEADER = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #141820, stop:0.5 #1a1f2e, stop:1 #141820)"
GRADIENT_CARD = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #262e42, stop:1 #1e2435)"

STATUS_COLORS = {
    "info": TEXT_SECONDARY,
    "success": CYAN,
    "warning": AMBER,
    "error": ROSE,
    "loading": ACCENT_LIGHT,
}

STATUS_ICONS = {
    "info": "💡",
    "success": "✅",
    "warning": "⚠️",
    "error": "❌",
    "loading": "⏳",
}

# ─── Hoja de estilo global premium ───────────────────────────────────
GLOBAL_STYLESHEET = f"""
    /* ── Base ─────────────────────────────────── */
    QWidget {{
        background-color: {BG};
        color: {TEXT};
        font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
        font-size: 13px;
    }}

    /* ── Tabs ─────────────────────────────────── */
    QTabWidget {{
        background: transparent;
    }}

    QTabWidget::pane {{
        border: none;
        background: transparent;
        margin-top: 0px;
    }}

    QTabBar {{
        background: transparent;
    }}

    QTabBar::tab {{
        background: transparent;
        color: {TEXT_SECONDARY};
        padding: 14px 28px;
        margin-right: 2px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
        border: none;
        border-bottom: 3px solid transparent;
    }}

    QTabBar::tab:selected {{
        color: {TEXT};
        border-bottom: 3px solid {ACCENT};
    }}

    QTabBar::tab:hover:!selected {{
        color: {TEXT};
        border-bottom: 3px solid {SURFACE_HOVER};
    }}

    /* ── Input ────────────────────────────────── */
    QLineEdit {{
        background: {SURFACE};
        border: 2px solid {SURFACE_BORDER};
        border-radius: 12px;
        padding: 14px 20px;
        font-size: 15px;
        color: {TEXT};
        selection-background-color: {ACCENT};
    }}

    QLineEdit:focus {{
        border: 2px solid {ACCENT};
    }}

    QLineEdit::placeholder {{
        color: {TEXT_MUTED};
    }}

    /* ── Buttons ──────────────────────────────── */
    QPushButton {{
        background: {SURFACE};
        border: 1px solid {SURFACE_BORDER};
        border-radius: 10px;
        padding: 11px 22px;
        font-size: 13px;
        font-weight: 600;
        color: {TEXT};
        min-width: 90px;
    }}

    QPushButton:hover {{
        background: {SURFACE_HOVER};
        border: 1px solid {ACCENT};
    }}

    QPushButton:pressed {{
        background: {SURFACE};
    }}

    QPushButton:disabled {{
        color: {TEXT_MUTED};
        background: {BG_ELEVATED};
        border: 1px solid {BG_ELEVATED};
    }}

    QPushButton#primary {{
        background: {GRADIENT_ACCENT};
        color: white;
        font-weight: 700;
        border: none;
        padding: 12px 28px;
        font-size: 14px;
    }}

    QPushButton#primary:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7d75ff, stop:1 #1ae6be);
    }}

    QPushButton#primary:disabled {{
        background: {SURFACE};
        color: {TEXT_MUTED};
    }}

    QPushButton#accent {{
        background: {ACCENT};
        color: white;
        font-weight: 700;
        border: none;
    }}

    QPushButton#accent:hover {{
        background: {ACCENT_LIGHT};
    }}

    QPushButton#danger {{
        background: transparent;
        color: {ROSE};
        border: 1px solid {ROSE};
    }}

    QPushButton#danger:hover {{
        background: #ff6b6b20;
    }}

    QPushButton#ghost {{
        background: transparent;
        border: 1px solid {SURFACE_BORDER};
        color: {TEXT_SECONDARY};
    }}

    QPushButton#ghost:hover {{
        border: 1px solid {TEXT_SECONDARY};
        color: {TEXT};
    }}

    /* ── ScrollArea ───────────────────────────── */
    QScrollArea {{
        border: none;
        background: transparent;
    }}

    QScrollBar:vertical {{
        background: {BG_DARK};
        width: 10px;
        border-radius: 5px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background: {SURFACE_HOVER};
        min-height: 30px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {ACCENT};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: {BG_DARK};
        height: 10px;
        border-radius: 5px;
    }}

    QScrollBar::handle:horizontal {{
        background: {SURFACE_HOVER};
        min-width: 30px;
        border-radius: 5px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {ACCENT};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* ── CheckBox ─────────────────────────────── */
    QCheckBox {{
        spacing: 10px;
        color: {TEXT};
        font-size: 13px;
    }}

    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 2px solid {SURFACE_BORDER};
        border-radius: 6px;
        background: {SURFACE};
    }}

    QCheckBox::indicator:hover {{
        border: 2px solid {ACCENT};
    }}

    QCheckBox::indicator:checked {{
        background: {ACCENT};
        border: 2px solid {ACCENT};
        image: none;
    }}

    /* ── ProgressBar ──────────────────────────── */
    QProgressBar {{
        border: none;
        border-radius: 6px;
        text-align: center;
        background: {SURFACE};
        max-height: 12px;
        min-height: 12px;
    }}

    QProgressBar::chunk {{
        background: {GRADIENT_ACCENT};
        border-radius: 6px;
    }}

    /* ── ComboBox ─────────────────────────────── */
    QComboBox {{
        background: {SURFACE};
        border: 2px solid {SURFACE_BORDER};
        border-radius: 10px;
        padding: 10px 18px;
        min-width: 130px;
        color: {TEXT};
        font-weight: 500;
    }}

    QComboBox:hover {{
        border: 2px solid {ACCENT};
    }}

    QComboBox:focus {{
        border: 2px solid {ACCENT};
    }}

    QComboBox::drop-down {{
        border: none;
        padding-right: 10px;
    }}

    QComboBox QAbstractItemView {{
        background: {SURFACE};
        color: {TEXT};
        selection-background-color: {ACCENT};
        selection-color: white;
        border: 1px solid {SURFACE_BORDER};
        border-radius: 8px;
        padding: 4px;
        outline: none;
    }}

    /* ── GroupBox ──────────────────────────────── */
    QGroupBox {{
        border: 1px solid {SURFACE_BORDER};
        border-radius: 16px;
        margin-top: 24px;
        padding: 20px 16px 16px 16px;
        font-weight: 700;
        color: {TEXT};
        background: {BG_ELEVATED};
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 20px;
        padding: 2px 12px;
        color: {ACCENT_LIGHT};
        font-size: 14px;
    }}

    /* ── Slider ───────────────────────────────── */
    QSlider::groove:horizontal {{
        border: none;
        height: 6px;
        background: {SURFACE};
        border-radius: 3px;
    }}

    QSlider::handle:horizontal {{
        background: {ACCENT};
        border: 3px solid {BG};
        width: 18px;
        height: 18px;
        margin: -7px 0;
        border-radius: 10px;
    }}

    QSlider::handle:horizontal:hover {{
        background: {ACCENT_LIGHT};
    }}

    QSlider::sub-page:horizontal {{
        background: {GRADIENT_ACCENT};
        border-radius: 3px;
    }}

    /* ── MenuBar ──────────────────────────────── */
    QMenuBar {{
        background: {BG_DARK};
        color: {TEXT_SECONDARY};
        border: none;
        padding: 4px 8px;
        font-size: 12px;
        font-weight: 500;
    }}

    QMenuBar::item {{
        padding: 6px 14px;
        border-radius: 6px;
    }}

    QMenuBar::item:selected {{
        background: {SURFACE};
        color: {TEXT};
    }}

    QMenu {{
        background: {SURFACE};
        color: {TEXT};
        border: 1px solid {SURFACE_BORDER};
        border-radius: 10px;
        padding: 6px;
    }}

    QMenu::item {{
        padding: 8px 20px;
        border-radius: 6px;
    }}

    QMenu::item:selected {{
        background: {ACCENT};
        color: white;
    }}

    QMenu::separator {{
        height: 1px;
        background: {SURFACE_BORDER};
        margin: 4px 10px;
    }}

    /* ── ToolTip ──────────────────────────────── */
    QToolTip {{
        background: {SURFACE};
        color: {TEXT};
        border: 1px solid {SURFACE_BORDER};
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 12px;
    }}
"""


# ═════════════════════════════════════════════════════════════════════
# FUNCIONES DE ESTILO REUTILIZABLES
# ═════════════════════════════════════════════════════════════════════

def card_style() -> str:
    """Tarjeta de imagen con glass effect y hover premium."""
    return f"""
        QFrame {{
            background: {GRADIENT_CARD};
            border-radius: 16px;
            border: 1px solid {SURFACE_BORDER};
        }}
        QFrame:hover {{
            border: 1px solid {ACCENT};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                         stop:0 #2d3650, stop:1 #232a3b);
        }}
    """


def card_selected_style() -> str:
    """Tarjeta seleccionada con borde accent."""
    return f"""
        QFrame {{
            background: {GRADIENT_CARD};
            border-radius: 16px;
            border: 2px solid {ACCENT};
        }}
    """


def status_style(color: str) -> str:
    """Barra de estado con fondo sutil."""
    return f"""
        font-size: 12px;
        color: {color};
        padding: 10px 20px;
        background: {BG_DARK};
        border-top: 1px solid {SURFACE_BORDER};
        font-weight: 600;
        letter-spacing: 0.3px;
    """


def header_style() -> str:
    """Estilo del banner/header de la app."""
    return f"""
        QFrame {{
            background: {GRADIENT_HEADER};
            border: none;
            border-bottom: 1px solid {SURFACE_BORDER};
        }}
    """


def dialog_style() -> str:
    """Diálogo modal premium con bordes redondeados."""
    return f"""
        QDialog {{
            background: {BG};
            border: 1px solid {SURFACE_BORDER};
            border-radius: 16px;
        }}
        QLabel {{
            color: {TEXT};
            background: transparent;
        }}
        QPushButton {{
            background: {SURFACE};
            color: {TEXT};
            border: 1px solid {SURFACE_BORDER};
            border-radius: 10px;
            padding: 10px 22px;
            font-size: 13px;
            font-weight: 600;
            min-width: 100px;
        }}
        QPushButton:hover {{
            background: {SURFACE_HOVER};
            border: 1px solid {ACCENT};
        }}
    """


def search_card_placeholder_style() -> str:
    """Placeholder animado para carga de thumbnail."""
    return f"""
        background: {SURFACE};
        border-radius: 12px;
        color: {TEXT_MUTED};
        font-size: 22px;
    """


def gallery_empty_style() -> str:
    """Estilo para el mensaje de galería vacía."""
    return f"""
        font-size: 16px;
        color: {TEXT_MUTED};
        padding: 60px;
        background: transparent;
    """


def badge_style(color: str = ACCENT) -> str:
    """Badge/counter pill style."""
    return f"""
        background: {color};
        color: white;
        border-radius: 10px;
        padding: 3px 10px;
        font-size: 11px;
        font-weight: 700;
    """


def separator_style() -> str:
    """Línea separadora sutil."""
    return f"""
        background: {SURFACE_BORDER};
        max-height: 1px;
        min-height: 1px;
        border: none;
    """
