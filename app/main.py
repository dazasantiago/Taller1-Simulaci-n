"""Punto de entrada de la interfaz gráfica (Streamlit) — placeholder.

Ejecutar con:
    streamlit run app/main.py

Este archivo NO contiene lógica real todavía, solo el esqueleto mínimo
de la app y los TODO de las secciones que se construirán aquí más
adelante. Las funciones que esta interfaz invocará viven en `src/` (ver
`docs/README.md` para la firma y el contrato de retorno de cada una).
"""

from __future__ import annotations

import sys
from pathlib import Path

# `streamlit run app/main.py` agrega la carpeta `app/` a sys.path, no la
# raíz del repositorio. Este bloque agrega la raíz para poder hacer
# `from src...` sin necesidad de instalar el paquete.
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

import streamlit as st

# TODO: una vez implementadas en src/, importar aquí las funciones a usar, ej.:
# from src.generadores.cuadrados_medios import cuadrados_medios
# from src.generadores.congruencial import (
#     congruencial_lineal,
#     congruencial_multiplicativo,
#     congruencial_aditivo,
# )
# from src.generadores.distribuciones import generar_uniforme, generar_normal
# from src.validacion.pruebas_estadisticas import (
#     prueba_medias,
#     prueba_varianza,
#     prueba_chi_cuadrado,
#     prueba_ks,
#     prueba_poker,
#     prueba_rachas,
# )

st.title("Generadores y Validación de Números Pseudoaleatorios")

# TODO: Sección - selección del método de generación.
#   Selector (ej. st.selectbox) entre: Cuadrados Medios, Congruencial
#   Lineal, Congruencial Multiplicativo, Congruencial Aditivo, Uniforme,
#   Normal. Mostrar los inputs específicos de cada método (semilla, a,
#   c, m, n_digitos, semillas_iniciales, cantidad, etc.).

# TODO: Sección - carga de semillas.
#   Permitir cargar un archivo (.txt/.csv, ej. st.file_uploader) con
#   semillas (ver data/seeds/) o ingresarlas manualmente
#   (ej. st.number_input / st.text_input).

# TODO: Sección - selección de prueba(s) de validación.
#   Selector (ej. st.multiselect) entre: medias, varianza, chi-cuadrado,
#   Kolmogorov-Smirnov, póker, rachas. Mostrar los parámetros
#   específicos de cada prueba (nivel de confianza, n_intervalos,
#   tam_mano).

# TODO: Sección - ejecución y visualización de resultados.
#   Botón para ejecutar (ej. st.button), mostrar la secuencia generada
#   en una tabla (ej. st.dataframe) y los resultados de cada prueba:
#   estadístico, valor crítico/p-valor, decisión (ej. st.metric /
#   st.write) y el gráfico correspondiente (ej. st.pyplot con la figura
#   devuelta por cada prueba_*).
