import pandas as pd
import streamlit as st

from app import estado
from src import estudio, graficas


def mostrar():
    resultados_sin_vacunacion = estado.resultados_sin_vacunacion()
    resultados_con_vacunacion = estado.resultados_con_vacunacion()

    if resultados_sin_vacunacion is None or resultados_con_vacunacion is None:
        st.info("Primero corre el estudio en la pestaña «Ejecución».")
        return

    dias = list(range(len(resultados_con_vacunacion[0]["historial_i"])))

    curvas = {}
    campos_por_estado = (("S", "historial_s"), ("E", "historial_e"), ("I", "historial_i"), ("R", "historial_r"))
    for nombre_estado, campo in campos_por_estado:
        curvas[nombre_estado] = estudio.calcular_curva_promedio(resultados_con_vacunacion, campo)

    st.subheader("Curva epidémica")
    st.pyplot(graficas.graficar_curva_epidemica(dias, curvas))

    st.subheader("Distribuciones")
    columna_izquierda, columna_derecha = st.columns(2)

    totales_infectados = []
    for resultado in resultados_con_vacunacion:
        totales_infectados.append(resultado["total_infectados"])

    dias_pico = []
    for resultado in resultados_con_vacunacion:
        dias_pico.append(resultado["dia_pico"])

    magnitudes_pico = []
    for resultado in resultados_con_vacunacion:
        magnitudes_pico.append(resultado["magnitud_pico"])

    dias_control = estudio.dias_hasta_control_validos(resultados_con_vacunacion)

    with columna_izquierda:
        st.pyplot(graficas.graficar_histograma(totales_infectados, "Total de infectados", "Total de infectados"))
        st.pyplot(graficas.graficar_histograma(dias_pico, "Día del pico de infectados", "Día del pico"))

    with columna_derecha:
        st.pyplot(graficas.graficar_histograma(magnitudes_pico, "Magnitud del pico de infectados", "Infectados en el pico"))
        if len(dias_control) > 0:
            st.pyplot(graficas.graficar_histograma(dias_control, "Días hasta el control del brote", "Día de control"))
        else:
            st.warning("Ninguna simulación controló el brote (I=0) dentro del horizonte de días.")

    st.subheader("Comparación de escenarios")
    promedio_i_sin, _, _ = estudio.calcular_curva_promedio(resultados_sin_vacunacion, "historial_i")
    promedio_i_con, _, _ = estudio.calcular_curva_promedio(resultados_con_vacunacion, "historial_i")
    st.pyplot(graficas.graficar_comparacion_escenarios(dias, promedio_i_sin, promedio_i_con))

    st.subheader("Estadísticas descriptivas por escenario")
    fila_sin = estudio.calcular_estadisticas_escenario(resultados_sin_vacunacion)
    fila_con = estudio.calcular_estadisticas_escenario(resultados_con_vacunacion)
    fila_sin["escenario"] = "Sin vacunación"
    fila_con["escenario"] = "Con vacunación"
    tabla = pd.DataFrame([fila_sin, fila_con])
    st.dataframe(tabla, hide_index=True)
