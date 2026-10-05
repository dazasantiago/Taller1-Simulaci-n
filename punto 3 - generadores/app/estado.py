from __future__ import annotations

import streamlit as st


def secuencias() -> list[dict]:
    return st.session_state.setdefault("secuencias", [])


def agregar(metodo: str, prefijo: str, parametros: dict, valores: list[float]) -> dict:
    contadores = st.session_state.setdefault("contadores", {})
    contadores[prefijo] = contadores.get(prefijo, 0) + 1
    secuencia = {
        "id": f"{prefijo}-{contadores[prefijo]}",
        "grupo": prefijo,
        "metodo": metodo,
        "parametros": parametros,
        "valores": valores,
        "resultados": {},
    }
    secuencias().append(secuencia)
    return secuencia


def buscar(id_secuencia: str) -> dict | None:
    return next((s for s in secuencias() if s["id"] == id_secuencia), None)


def agrupadas() -> dict[str, list[dict]]:
    grupos: dict[str, list[dict]] = {}
    for s in secuencias():
        grupos.setdefault(s["grupo"], []).append(s)
    return grupos


def descripcion(secuencia: dict) -> str:
    partes = [f"{k}={v}" for k, v in secuencia["parametros"].items()]
    partes.append(f"n={len(secuencia['valores'])}")
    return ", ".join(partes)


def vaciar() -> None:
    st.session_state["secuencias"] = []
    st.session_state["contadores"] = {}
