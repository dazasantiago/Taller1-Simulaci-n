from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

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
