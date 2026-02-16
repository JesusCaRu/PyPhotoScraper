"""
Workers para la búsqueda de imágenes en diferentes motores.
Se ejecutan en hilos secundarios (QThread) para no bloquear la interfaz.
"""
import re
import json
import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal

# User-Agent realista para evitar bloqueos
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
}


class SearchWorker(QThread):
    """Hilo que busca URLs de imágenes en el motor seleccionado."""

    finished = pyqtSignal(list)   # lista de URLs encontradas
    error = pyqtSignal(str)       # mensaje de error

    def __init__(self, query: str, engine: str, options: dict):
        super().__init__()
        self.query = query
        self.engine = engine
        self.options = options

    # ── Ejecución del hilo ───────────────────────────────────────────
    def run(self):
        try:
            engines = {
                "google": self._search_google,
                "bing": self._search_bing,
                "duckduckgo": self._search_duckduckgo,
            }
            fn = engines.get(self.engine, self._search_google)
            images = fn()
            self.finished.emit(images)
        except Exception as e:
            self.error.emit(str(e))

    # ── Google Images ────────────────────────────────────────────────
    def _search_google(self) -> list[str]:
        url = f"https://www.google.com/search?q={self.query.replace(' ', '+')}&tbm=isch"

        tbs_parts: list[str] = []
        size_map = {"Grande": "isz:l", "Mediano": "isz:m", "Pequeño": "isz:i"}
        color_map = {
            "Blanco y negro": "ic:gray",
            "Transparente": "ic:trans",
            "Rojo": "ic:specific,isc:red",
            "Azul": "ic:specific,isc:blue",
            "Verde": "ic:specific,isc:green",
        }

        if self.options.get("size") in size_map:
            tbs_parts.append(size_map[self.options["size"]])
        if self.options.get("color") in color_map:
            tbs_parts.append(color_map[self.options["color"]])
        if tbs_parts:
            url += f"&tbs={','.join(tbs_parts)}"
        if self.options.get("safe"):
            url += "&safe=active"

        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        images: list[str] = []

        # Thumbnails directos
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or img.get("data-iurl")
            if src and src.startswith("http") and "google" not in src:
                images.append(src)

        # URLs de alta resolución incrustadas en scripts
        pattern = re.compile(
            r'\["(https?://[^"]+\.(?:jpg|jpeg|png|gif|webp))",\s*\d+,\s*\d+\]'
        )
        for match in pattern.findall(response.text):
            if match not in images:
                images.append(match)

        return images[:50]

    # ── Bing Images ──────────────────────────────────────────────────
    def _search_bing(self) -> list[str]:
        url = f"https://www.bing.com/images/search?q={self.query.replace(' ', '+')}"
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        images: list[str] = []

        # Método 1: enlaces con metadatos JSON
        for a_tag in soup.find_all("a", class_="iusc"):
            try:
                meta = json.loads(a_tag.get("m", "{}"))
                if "murl" in meta:
                    images.append(meta["murl"])
            except (json.JSONDecodeError, TypeError):
                continue

        # Método 2: fallback a thumbnails directos
        if not images:
            for img in soup.find_all("img", class_="mimg"):
                src = img.get("src") or img.get("data-src")
                if src and src.startswith("http"):
                    images.append(src)

        return images[:50]

    # ── DuckDuckGo Images ────────────────────────────────────────────
    def _search_duckduckgo(self) -> list[str]:
        try:
            # Obtener token VQD necesario para la API de imágenes
            res = requests.post(
                "https://duckduckgo.com/",
                data={"q": self.query},
                headers=HEADERS,
                timeout=10,
            )
            vqd_match = re.search(r"vqd=([^&]+)&", res.text)
            if not vqd_match:
                return []
            vqd = vqd_match.group(1)

            headers = {**HEADERS, "Referer": "https://duckduckgo.com/"}
            api_url = (
                f"https://duckduckgo.com/i.js?l=us-en&o=json"
                f"&q={self.query}&vqd={vqd}&f=,,,&p=1"
            )
            res = requests.get(api_url, headers=headers, timeout=10)
            data = res.json()
            return [img["image"] for img in data.get("results", [])][:50]
        except Exception:
            return []
