"""Punto de entrada de la interfaz gráfica (Streamlit).

Ejecutar con:
    streamlit run app/main.py

Solo orquesta: la lógica de generación y validación vive en `src/` (ver
`docs/README.md`) y se consume a través de `app/catalogo.py`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Las pruebas crean figuras con pyplot; sin backend gráfico evita problemas
# de hilos en Streamlit.
os.environ.setdefault("MPLBACKEND", "Agg")

# `streamlit run app/main.py` agrega la carpeta `app/` a sys.path, no la
# raíz del repositorio. Este bloque agrega la raíz para poder hacer
# `from src...` y `from app...` sin necesidad de instalar el paquete.
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

import streamlit as st

from app import tab_generacion, tab_validacion

st.set_page_config(page_title="Generadores y Validación", layout="wide")
st.title("Generadores y Validación de Números Pseudoaleatorios")

pestana_generacion, pestana_validacion = st.tabs(["Generación", "Validación"])
with pestana_generacion:
    tab_generacion.mostrar()
with pestana_validacion:
    tab_validacion.mostrar()
