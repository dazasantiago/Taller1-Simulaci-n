import streamlit as st

from app import estado
from src import configuracion


def mostrar():
    st.subheader("Parámetros de la simulación")

    archivo = st.file_uploader("Cargar configuración (.csv)", type=["csv"])
    if archivo is not None:
        texto = archivo.getvalue().decode("utf-8-sig")
        parametros = configuracion.leer_configuracion_texto(texto)
        st.success("Configuración cargada desde archivo.")
    else:
        parametros = configuracion.parametros_por_defecto()
        st.info("Usando la configuración por defecto (ver configuracion_ejemplo.csv).")

    columna_izquierda, columna_derecha = st.columns(2)

    with columna_izquierda:
        st.metric("Población (N)", parametros["n_poblacion"])
        st.metric("Infectados iniciales", parametros["infectados_iniciales"])
        st.metric("Días por simulación", parametros["dias_simulacion"])

    with columna_derecha:
        parametros["n_simulaciones"] = st.number_input(
            "Simulaciones por escenario",
            min_value=1,
            max_value=2000,
            value=parametros["n_simulaciones"],
            step=1,
        )
        semilla = st.number_input("Semilla inicial", min_value=1, value=12345, step=1)

    st.write("Rango de β (tasa de contacto):", parametros["rango_beta"])
    st.write("Rango de σ⁻¹ (incubación, días):", parametros["rango_sigma"])
    st.write("Rango de γ⁻¹ (infeccioso, días):", parametros["rango_gamma"])
    st.write("Rango de p (probabilidad de transmisión):", parametros["rango_p_transmision"])
    st.write("Rango de tasa de vacunación:", parametros["rango_tasa_vacunacion"])
    st.write("Rango de efectividad de la vacuna:", parametros["rango_efectividad_vacuna"])

    if st.button("Guardar configuración", type="primary"):
        estado.guardar_parametros(parametros, semilla)
        st.success("Configuración guardada. Ve a la pestaña «Ejecución».")
