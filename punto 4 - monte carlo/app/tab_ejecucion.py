import time

import streamlit as st

from app import estado
from src import simulacion
from src.generadores import generador_temporal


def mostrar():
    st.subheader("Ejecutar estudio")

    parametros = estado.parametros_actuales()
    if parametros is None:
        st.info("Primero guarda una configuración en la pestaña «Configuración».")
        return

    n_simulaciones = parametros["n_simulaciones"]
    semilla = estado.semilla_actual()

    st.write(
        f"Se van a correr {n_simulaciones} simulaciones sin vacunación y "
        f"{n_simulaciones} con vacunación, de {parametros['dias_simulacion']} días cada una."
    )

    if st.button("Correr estudio completo", type="primary"):
        inicio = time.time()
        barra = st.progress(0.0)
        total_corridas = n_simulaciones * 2

        generador_temporal.inicializar(semilla)
        resultados_sin_vacunacion = []
        for i in range(n_simulaciones):
            resultado = simulacion.correr_una_simulacion(
                parametros, generador_temporal.siguiente_uniforme, forzar_sin_vacunacion=True
            )
            resultados_sin_vacunacion.append(resultado)
            barra.progress((i + 1) / total_corridas)

        generador_temporal.inicializar(semilla + 10_000_000)
        resultados_con_vacunacion = []
        for i in range(n_simulaciones):
            resultado = simulacion.correr_una_simulacion(
                parametros, generador_temporal.siguiente_uniforme, forzar_sin_vacunacion=False
            )
            resultados_con_vacunacion.append(resultado)
            barra.progress((n_simulaciones + i + 1) / total_corridas)

        estado.guardar_resultados(resultados_sin_vacunacion, resultados_con_vacunacion)

        duracion_segundos = time.time() - inicio
        st.success(f"Estudio terminado en {duracion_segundos:.1f} segundos. Ve a «Resultados».")
