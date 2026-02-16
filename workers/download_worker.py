"""
Workers para descarga de imágenes y carga de miniaturas.
Se ejecutan en hilos secundarios (QThread) para no bloquear la interfaz.

NOTA IMPORTANTE: QPixmap NO se puede crear en un hilo secundario.
En su lugar se emiten los bytes crudos y el hilo principal crea el QPixmap.
"""
import os
import time
import requests
from PyQt5.QtCore import QThread, pyqtSignal


class ImageDownloader(QThread):
    """Descarga una lista de imágenes a una carpeta local."""

    progress = pyqtSignal(int, int)   # (actual, total)
    finished = pyqtSignal(int)        # cantidad de descargas exitosas
    error = pyqtSignal(str)

    def __init__(self, urls: list[str], folder: str, prefix: str):
        super().__init__()
        self.urls = urls
        self.folder = folder
        self.prefix = prefix

    def run(self):
        success = 0
        total = len(self.urls)
        os.makedirs(self.folder, exist_ok=True)

        for i, url in enumerate(self.urls):
            try:
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    # Detectar extensión por Content-Type
                    ct = response.headers.get("Content-Type", "")
                    ext = "jpg"
                    if "png" in ct:
                        ext = "png"
                    elif "gif" in ct:
                        ext = "gif"
                    elif "webp" in ct:
                        ext = "webp"

                    filename = f"{self.prefix}_{int(time.time())}_{i}.{ext}"
                    path = os.path.join(self.folder, filename)

                    with open(path, "wb") as f:
                        f.write(response.content)
                    success += 1

                self.progress.emit(i + 1, total)
            except Exception as e:
                print(f"[Download] Error ({url[:60]}...): {e}")

        self.finished.emit(success)


class ThumbnailLoader(QThread):
    """
    Descarga la imagen de una URL y emite los bytes crudos.
    El QPixmap se debe crear en el hilo principal (slot conectado).
    """

    loaded = pyqtSignal(bytes, int)  # (datos de imagen, índice)
    failed = pyqtSignal(int)         # índice que falló

    def __init__(self, url: str, index: int):
        super().__init__()
        self.url = url
        self.index = index

    def run(self):
        try:
            response = requests.get(self.url, timeout=8)
            if response.status_code == 200 and len(response.content) > 100:
                self.loaded.emit(response.content, self.index)
            else:
                self.failed.emit(self.index)
        except Exception:
            self.failed.emit(self.index)
