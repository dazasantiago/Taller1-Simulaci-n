import streamlit as st


def parametros_actuales():
    return st.session_state.get("parametros")


def guardar_parametros(parametros, semilla):
    st.session_state["parametros"] = parametros
    st.session_state["semilla"] = semilla


def semilla_actual():
    return st.session_state.get("semilla", 12345)


def resultados_sin_vacunacion():
    return st.session_state.get("resultados_sin_vacunacion")


def resultados_con_vacunacion():
    return st.session_state.get("resultados_con_vacunacion")


def guardar_resultados(resultados_sin_vacunacion, resultados_con_vacunacion):
    st.session_state["resultados_sin_vacunacion"] = resultados_sin_vacunacion
    st.session_state["resultados_con_vacunacion"] = resultados_con_vacunacion
