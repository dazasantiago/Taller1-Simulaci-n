"""Pestaña "Generación": elegir un método, sus parámetros y semillas, y generar."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from matplotlib.figure import Figure

from app import catalogo, estado, semillas


def _campo(campo: catalogo.Campo, clave: str):
    """Renderiza un number_input del tipo (int/float) que corresponda al campo."""
    entero = isinstance(campo.defecto, int)
    return st.number_input(
        campo.etiqueta,
        value=campo.defecto,
        min_value=campo.minimo,
        max_value=campo.maximo,
        step=1 if entero else 0.01,
        format="%d" if entero else "%.3f",
        key=f"{clave}_{campo.nombre}",
    )


def _entrada_semillas(clave: str, base: catalogo.Base) -> list[int] | None:
    """Semillas manuales o importadas. Devuelve None si el texto es inválido."""
    if base.vectorial:
        st.caption(
            "En este método la semilla es un **vector**: todas las semillas "
            "ingresadas forman los valores iniciales de **una sola** secuencia "
            "(mínimo 2)."
        )
    else:
        st.caption("Se generará **una secuencia por cada semilla**, con los parámetros de arriba.")

    clave_texto = f"{clave}_semillas"
    st.session_state.setdefault(clave_texto, "")

    archivo = st.file_uploader(
        "Importar semillas (.txt o .csv)", type=["txt", "csv"], key=f"{clave}_archivo"
    )
    if archivo is not None and st.session_state.get(f"{clave}_archivo_id") != archivo.file_id:
        try:
            importadas = semillas.leer_archivo(archivo.name, archivo.getvalue())
        except ValueError as exc:
            st.error(f"No se pudo leer '{archivo.name}': {exc}.")
        else:
            st.session_state[clave_texto] = ", ".join(str(s) for s in importadas)
            st.session_state[f"{clave}_archivo_id"] = archivo.file_id

    texto = st.text_area(
        "Semillas (enteros separados por comas, espacios o saltos de línea)",
        key=clave_texto,
        placeholder="Ej.: 5735, 1234, 9876",
    )
    try:
        lista = semillas.parsear_texto(texto)
    except ValueError as exc:
        st.error(f"Semillas inválidas: {exc}.")
        return None
    if base.vectorial and 0 < len(lista) < 2:
        st.warning("El congruencial aditivo necesita al menos 2 semillas.")
        return None
    return lista


def _formulario_generacion() -> None:
    metodos = catalogo.metodos_disponibles()
    if not metodos:
        st.info(
            "Todavía no hay generadores implementados en `src/generadores/`. "
            "Cuando estén listos aparecerán aquí automáticamente."
        )
        return

    metodo = st.selectbox("Método de generación", metodos, format_func=lambda m: m.etiqueta)
    base = metodo.base
    if metodo.normal:
        base = st.selectbox(
            "Método base (genera los uniformes que transforma Box-Muller)",
            catalogo.bases_disponibles(),
            format_func=lambda b: b.etiqueta,
        )

    clave = f"{metodo.id}_{base.id}"
    columnas = st.columns(len(base.campos) + 1)
    campos = {}
    for columna, campo in zip(columnas, base.campos):
        with columna:
            campos[campo.nombre] = _campo(campo, clave)
    with columnas[-1]:
        cantidad = st.number_input(
            "Cantidad de números", value=1000, min_value=10, step=100, key=f"{clave}_cantidad"
        )

    lista = _entrada_semillas(clave, base)

    if st.button("Generar", type="primary", disabled=not lista, key=f"{clave}_generar"):
        # Aditivo: un solo vector; los demás: una secuencia por semilla.
        entradas = [lista] if base.vectorial else lista
        generadas, fallos = 0, []
        with st.spinner("Generando..."):
            for semilla in entradas:
                parametros = catalogo.parametros_base(base, campos, semilla)
                try:
                    valores = catalogo.generar(metodo, base, parametros, int(cantidad))
                except Exception as exc:
                    fallos.append(f"semilla {semilla}: {type(exc).__name__}: {exc}")
                    continue
                if metodo.normal:
                    parametros = {"base": base.etiqueta, **parametros}
                estado.agregar(metodo.etiqueta, metodo.prefijo, parametros, valores)
                generadas += 1
        if generadas:
            st.success(f"Se guardaron {generadas} secuencia(s) en memoria.")
        for fallo in fallos:
            st.error(f"No se pudo generar con {fallo}")


def _histograma(valores: list[float], intervalos: int, titulo: str) -> Figure:
    fig = Figure(figsize=(6, 3.6))
    ax = fig.subplots()
    ax.hist(valores, bins=intervalos, edgecolor="white")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frecuencia")
    ax.set_title(titulo)
    fig.tight_layout()
    return fig


def _secuencias_en_memoria() -> None:
    guardadas = estado.secuencias()
    st.subheader(f"Secuencias en memoria ({len(guardadas)})")
    if not guardadas:
        st.caption("Aún no se ha generado ninguna secuencia.")
        return

    izquierda, derecha = st.columns([4, 1])
    with izquierda:
        elegida = st.selectbox(
            "Ver secuencia",
            guardadas,
            index=len(guardadas) - 1,
            format_func=lambda s: f"{s['id']} · {s['metodo']} · {estado.descripcion(s)}",
        )
    with derecha:
        st.write("")  # alinea el botón con el selectbox
        if st.button("Vaciar memoria"):
            estado.vaciar()
            st.rerun()

    valores = elegida["valores"]
    tabla = pd.DataFrame({"i": range(1, len(valores) + 1), "valor": valores})
    tabla_col, grafico_col = st.columns(2)
    with tabla_col:
        st.dataframe(tabla, hide_index=True, height=360)
        st.download_button(
            "Exportar CSV",
            tabla.to_csv(index=False).encode("utf-8"),
            file_name=f"{elegida['id']}.csv",
            mime="text/csv",
        )
    with grafico_col:
        intervalos = st.number_input(
            "Intervalos del histograma", value=10, min_value=2, max_value=200, step=1
        )
        st.pyplot(_histograma(valores, int(intervalos), f"Histograma · {elegida['id']}"))


def mostrar() -> None:
    _formulario_generacion()
    st.divider()
    _secuencias_en_memoria()
