import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

import streamlit as st

from app import tab_configuracion, tab_ejecucion, tab_resultados, tab_sensibilidad

st.set_page_config(page_title="EpiSim - Montecarlo SEIR", layout="wide")
st.title("EpiSim: Simulación Montecarlo de Propagación de Enfermedad")

pestana_configuracion, pestana_ejecucion, pestana_resultados, pestana_sensibilidad = st.tabs(
    ["Configuración", "Ejecución", "Resultados", "Sensibilidad"]
)

with pestana_configuracion:
    tab_configuracion.mostrar()
with pestana_ejecucion:
    tab_ejecucion.mostrar()
with pestana_resultados:
    tab_resultados.mostrar()
with pestana_sensibilidad:
    tab_sensibilidad.mostrar()
