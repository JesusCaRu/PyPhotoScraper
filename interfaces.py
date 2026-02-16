"""
Visual Gallery Explorer Pro
Este archivo existe por compatibilidad.
Ejecuta main.py para la versión refactorizada.
"""
import sys
import os

# Añadir directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    main()