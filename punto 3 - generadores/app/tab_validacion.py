"""Pestaña "Validación": secuencias en memoria agrupadas por método y sus pruebas."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from matplotlib.figure import Figure

from app import catalogo, estado

_LLAVES_FIGURA = ("figure", "figura")
_LLAVES_VEREDICTO = ("passes_test", "pasa_prueba")
_ESCALARES = (int, float, str, bool, np.number, np.bool_)


def _veredicto(resultado: dict) -> bool | None:
    for llave in _LLAVES_VEREDICTO:
        if llave in resultado:
            return bool(resultado[llave])
    return None


def _formatear(valor) -> str:
    if isinstance(valor, (float, np.floating)):
        return f"{valor:.6g}"
    return str(valor)


def _mostrar_resultado(resultado: dict) -> None:
    if "error" in resultado:
        st.error(f"La prueba falló: {resultado['error']}")
        return

    veredicto = _veredicto(resultado)
    if veredicto is True:
        st.success("Pasa la prueba (no se rechaza H0).")
    elif veredicto is False:
        st.error("No pasa la prueba (se rechaza H0).")

    ocultas = set(_LLAVES_FIGURA) | set(_LLAVES_VEREDICTO)
    escalares = {k: v for k, v in resultado.items() if k not in ocultas and isinstance(v, _ESCALARES)}
    detalle = {
        k: v
        for k, v in resultado.items()
        if k not in ocultas and k not in escalares and isinstance(v, (list, tuple, dict, np.ndarray))
    }

    if escalares:
        st.dataframe(
            pd.DataFrame({"Métrica": list(escalares), "Valor": [_formatear(v) for v in escalares.values()]}),
            hide_index=True,
        )
    for llave, valor in detalle.items():
        with st.expander(llave):
            st.write(valor)

    for llave in _LLAVES_FIGURA:
        if isinstance(resultado.get(llave), Figure):
            st.pyplot(resultado[llave])
            break


@st.dialog("Seleccionar pruebas")
def _dialogo_pruebas(ids: list[str], objetivo: str) -> None:
    st.write(f"Se aplicarán a **{objetivo}** ({len(ids)} secuencia(s)).")
    disponibles = catalogo.pruebas_disponibles()
    elegidas = st.multiselect(
        "Pruebas a ejecutar",
        disponibles,
        default=disponibles,
        format_func=lambda p: p.etiqueta,
    )

    parametros: dict[str, dict] = {}
    for prueba in elegidas:
        campos = catalogo.campos_aceptados(prueba)
        if not campos:
            continue
        st.markdown(f"**{prueba.etiqueta}**")
        parametros[prueba.id] = {}
        for campo in campos:
            entero = isinstance(campo.defecto, int)
            parametros[prueba.id][campo.nombre] = st.number_input(
                campo.etiqueta,
                value=campo.defecto,
                min_value=campo.minimo,
                max_value=campo.maximo,
                step=1 if entero else 0.01,
                format="%d" if entero else "%.3f",
                key=f"par_{prueba.id}_{campo.nombre}",
            )

    if st.button("Ejecutar", type="primary", disabled=not elegidas):
        total = len(ids) * len(elegidas)
        barra = st.progress(0.0)
        hechas = 0
        for id_secuencia in ids:
            secuencia = estado.buscar(id_secuencia)
            for prueba in elegidas:
                secuencia["resultados"][prueba.id] = catalogo.ejecutar_prueba(
                    prueba, secuencia["valores"], parametros.get(prueba.id, {})
                )
                hechas += 1
                barra.progress(hechas / total)
        st.rerun()


@st.dialog("Resultados", width="large")
def _dialogo_resultados(id_secuencia: str) -> None:
    secuencia = estado.buscar(id_secuencia)
    st.write(f"**{secuencia['id']}** · {secuencia['metodo']} · {estado.descripcion(secuencia)}")
    etiquetas = {p.id: p.etiqueta for p in catalogo.PRUEBAS}
    resultados = secuencia["resultados"]
    pestanas = st.tabs([etiquetas[pid] for pid in resultados])
    for pestana, resultado in zip(pestanas, resultados.values()):
        with pestana:
            _mostrar_resultado(resultado)


def _estado_pruebas(secuencia: dict) -> str:
    if not secuencia["resultados"]:
        return "Sin probar"
    etiquetas = {p.id: p.etiqueta.removeprefix("Prueba de ").removeprefix("Prueba ") for p in catalogo.PRUEBAS}
    iconos = {True: "✅", False: "❌", None: "⚠️"}
    return " · ".join(
        f"{etiquetas[pid]} {iconos[_veredicto(r) if 'error' not in r else None]}"
        for pid, r in secuencia["resultados"].items()
    )


def mostrar() -> None:
    grupos = estado.agrupadas()
    if not grupos:
        st.info("Aún no hay secuencias. Genera alguna en la pestaña «Generación».")
        return
    if not catalogo.pruebas_disponibles():
        st.info(
            "Todavía no hay pruebas implementadas en `src/validacion/`. "
            "Cuando estén listas aparecerán aquí automáticamente."
        )
        return

    todas = [s["id"] for lista in grupos.values() for s in lista]
    if st.button("Probar todas las generaciones", type="primary"):
        _dialogo_pruebas(todas, "todas las generaciones")

    for prefijo, lista in grupos.items():
        with st.expander(f"{prefijo} · {lista[0]['metodo']} ({len(lista)})", expanded=True):
            if st.button("Probar este grupo", key=f"grupo_{prefijo}"):
                _dialogo_pruebas([s["id"] for s in lista], f"el grupo {prefijo}")
            for s in lista:
                c_id, c_desc, c_estado, c_probar, c_res = st.columns([1, 4, 4, 1.4, 1.6])
                c_id.markdown(f"**{s['id']}**")
                c_desc.caption(estado.descripcion(s))
                c_estado.caption(_estado_pruebas(s))
                if c_probar.button("Probar", key=f"probar_{s['id']}"):
                    _dialogo_pruebas([s["id"]], f"la secuencia {s['id']}")
                if s["resultados"] and c_res.button("Resultados", key=f"res_{s['id']}"):
                    _dialogo_resultados(s["id"])
