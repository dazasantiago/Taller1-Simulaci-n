import pandas as pd
import streamlit as st

from app import estado
from src import estudio, graficas


def mostrar():
    resultados_con_vacunacion = estado.resultados_con_vacunacion()
    if resultados_con_vacunacion is None:
        st.info("Primero corre el estudio en la pestaña «Ejecución».")
        return

    filas = estudio.analizar_sensibilidad(resultados_con_vacunacion)

    st.subheader("Impacto de cada parámetro en el total de infectados")
    st.pyplot(graficas.graficar_tornado(filas))

    tabla = pd.DataFrame(filas)
    st.dataframe(tabla, hide_index=True)
