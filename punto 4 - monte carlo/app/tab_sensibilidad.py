import pandas as pd
import streamlit as st

from app import estado
from src import estudio, graficas


def mostrar():
    resultados_con_vacunacion = estado.resultados_con_vacunacion()
    if resultados_con_vacunacion is None:
        st.info("Primero corre el estudio en la pestaña «Ejecución».")
        return

    opciones_metrica = {"Total de infectados": "total_infectados", "Total de muertes": "total_muertes"}
    etiqueta_metrica = st.radio("Métrica de impacto", list(opciones_metrica.keys()), horizontal=True)
    campo_objetivo = opciones_metrica[etiqueta_metrica]

    filas = estudio.analizar_sensibilidad(resultados_con_vacunacion, campo_objetivo)

    st.subheader(f"Impacto de cada parámetro en {etiqueta_metrica.lower()}")
    st.pyplot(graficas.graficar_tornado(filas))

    tabla = pd.DataFrame(filas)
    st.dataframe(tabla, hide_index=True)
