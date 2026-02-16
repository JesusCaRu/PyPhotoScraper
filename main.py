"""
Visual Gallery Explorer Pro - Punto de entrada principal.
Aplicación moderna para buscar, explorar y descargar imágenes de la web.
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor, QPalette
from ui.main_window import MainWindow


def setup_palette(app: QApplication):
    """Configura la paleta de colores oscura premium para toda la aplicación."""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(26, 31, 46))       # BG
    palette.setColor(QPalette.WindowText, QColor(232, 234, 240)) # TEXT
    palette.setColor(QPalette.Base, QColor(35, 42, 59))          # SURFACE
    palette.setColor(QPalette.AlternateBase, QColor(42, 51, 72))
    palette.setColor(QPalette.ToolTipBase, QColor(35, 42, 59))
    palette.setColor(QPalette.ToolTipText, QColor(232, 234, 240))
    palette.setColor(QPalette.Text, QColor(232, 234, 240))
    palette.setColor(QPalette.Button, QColor(48, 58, 82))
    palette.setColor(QPalette.ButtonText, QColor(232, 234, 240))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, QColor(108, 99, 255))        # ACCENT
    palette.setColor(QPalette.Highlight, QColor(108, 99, 255))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    setup_palette(app)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
