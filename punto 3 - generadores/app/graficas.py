"""Generación de gráficos para las pruebas de validación en la capa de interfaz (Vista).

Mantiene desacoplada la lógica estadística (src/validacion/) de la capa gráfica.
"""

from __future__ import annotations

import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from scipy.stats import chi2, norm


def graficar_medias(resultado: dict) -> Figure:
    """Genera el gráfico para la prueba de medias: distribución muestral, límites y media observada."""
    n = resultado.get("n", 1000)
    se = resultado.get("standard_error")
    mean = resultado.get("mean", resultado.get("promedio", 0.5))
    lower_bound = resultado.get("lower_bound", resultado.get("limite_inferior", 0.45))
    upper_bound = resultado.get("upper_bound", resultado.get("limite_superior", 0.55))
    passed = resultado.get("passes_test", resultado.get("passed_test", True))
    a = resultado.get("alpha", 0.05)

    if se is None or se <= 0:
        se = (upper_bound - lower_bound) / (2 * 1.95996) if upper_bound > lower_bound else 0.01

    fig, ax = plt.subplots(figsize=(7, 4.2))
    x_min = min(0.5 - 3.5 * se, mean - 0.5 * se, lower_bound - 0.5 * se)
    x_max = max(0.5 + 3.5 * se, mean + 0.5 * se, upper_bound + 0.5 * se)
    x = np.linspace(x_min, x_max, 400)
    y = norm.pdf(x, 0.5, se)

    ax.plot(x, y, color="#2b5c8f", lw=2, label="Dist. muestral teórica N(0.5, 1/(12n))")

    # Región de aceptación
    x_ci = np.linspace(lower_bound, upper_bound, 200)
    ax.fill_between(
        x_ci,
        norm.pdf(x_ci, 0.5, se),
        color="#2ca02c",
        alpha=0.2,
        label=f"Zona de aceptación ({int(round((1 - a) * 100))}%)",
    )

    # Líneas de referencia
    ax.axvline(lower_bound, color="#2ca02c", linestyle="--", lw=1.5, label=f"Límite inf. = {lower_bound:.5f}")
    ax.axvline(upper_bound, color="#2ca02c", linestyle="--", lw=1.5, label=f"Límite sup. = {upper_bound:.5f}")
    ax.axvline(0.5, color="#111111", linestyle="-", lw=1.5, label="Media teórica = 0.50000")

    color_obs = "#2ca02c" if passed else "#d62728"
    estado_txt = "PASA" if passed else "NO PASA"
    ax.axvline(mean, color=color_obs, linestyle="-", lw=2.5, label=f"Media calculada = {mean:.5f} ({estado_txt})")

    ax.set_title("Prueba de Medias - Distribución e Intervalo de Confianza")
    ax.set_xlabel("Media Muestral")
    ax.set_ylabel("Densidad de Probabilidad")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig


def graficar_varianza(resultado: dict) -> Figure:
    """Genera el gráfico para la prueba de varianza: distribución muestral, límites y varianza observada."""
    variance = resultado.get("variance", resultado.get("varianza", 1.0 / 12.0))
    lower_bound = resultado.get("lower_bound", resultado.get("limite_inferior", 0.07))
    upper_bound = resultado.get("upper_bound", resultado.get("limite_superior", 0.09))
    df = resultado.get("df", 999)
    a = resultado.get("alpha", 0.05)
    passed = resultado.get("passes_test", resultado.get("passed_test", True))
    theoretical_variance = resultado.get("theoretical_variance", 1.0 / 12.0)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    se_var = theoretical_variance * math.sqrt(2.0 / df) if df > 0 else 0.005
    scale = 1.0 / (12.0 * df) if df > 0 else 1.0

    x_min = max(0.0, min(lower_bound - 0.5 * se_var, variance - 0.5 * se_var, theoretical_variance - 3.5 * se_var))
    x_max = max(upper_bound + 0.5 * se_var, variance + 0.5 * se_var, theoretical_variance + 3.5 * se_var)
    x = np.linspace(x_min, x_max, 400)

    try:
        y = chi2.pdf(x, df=df, scale=scale)
        if np.any(np.isnan(y)) or np.all(y == 0):
            y = norm.pdf(x, theoretical_variance, se_var)
    except Exception:
        y = norm.pdf(x, theoretical_variance, se_var)

    ax.plot(x, y, color="#2b5c8f", lw=2, label="Dist. muestral teórica de S²")

    # Región de aceptación
    x_ci = np.linspace(lower_bound, upper_bound, 200)
    try:
        y_ci = chi2.pdf(x_ci, df=df, scale=scale)
        if np.any(np.isnan(y_ci)) or np.all(y_ci == 0):
            y_ci = norm.pdf(x_ci, theoretical_variance, se_var)
    except Exception:
        y_ci = norm.pdf(x_ci, theoretical_variance, se_var)

    ax.fill_between(
        x_ci,
        y_ci,
        color="#2ca02c",
        alpha=0.2,
        label=f"Zona de aceptación ({int(round((1 - a) * 100))}%)",
    )

    # Líneas de referencia
    ax.axvline(lower_bound, color="#2ca02c", linestyle="--", lw=1.5, label=f"Límite inf. = {lower_bound:.5f}")
    ax.axvline(upper_bound, color="#2ca02c", linestyle="--", lw=1.5, label=f"Límite sup. = {upper_bound:.5f}")
    ax.axvline(theoretical_variance, color="#111111", linestyle="-", lw=1.5, label=f"Varianza teórica = {theoretical_variance:.5f}")

    color_obs = "#2ca02c" if passed else "#d62728"
    estado_txt = "PASA" if passed else "NO PASA"
    ax.axvline(variance, color=color_obs, linestyle="-", lw=2.5, label=f"Varianza calculada = {variance:.5f} ({estado_txt})")

    ax.set_title("Prueba de Varianza - Distribución e Intervalo de Confianza")
    ax.set_xlabel("Varianza Muestral (S²)")
    ax.set_ylabel("Densidad de Probabilidad")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig


def graficar_ks(resultado: dict, secuencia: list[float] | None = None) -> Figure:
    """Genera el gráfico para Kolmogorov-Smirnov: FEC vs Teórica uniforme y máxima diferencia D_max."""
    d_max = resultado.get("d_max", resultado.get("statistic", 0.05))
    d_max_p = resultado.get("critical_value", resultado.get("valor_critico", 0.08))
    passed = resultado.get("passes_test", resultado.get("passed_test", True))
    intervals_table = resultado.get("intervals_table", resultado.get("tabla_intervalos", []))

    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Curva teórica uniforme F(x) = x en [0, 1]
    ax.plot([0, 1], [0, 1], color="#111111", linestyle="--", lw=1.5, label="F(x) Teórica Uniforme [0, 1]")

    if secuencia:
        seq_sorted = np.sort(secuencia)
        n = len(secuencia)
        fec_y = np.arange(1, n + 1) / n
        ax.step(seq_sorted, fec_y, where="post", color="#1f77b4", lw=1.5, alpha=0.7, label="FEC Empírica acumulada")

    if intervals_table:
        x_obs = [row.get("end", row.get("final")) for row in intervals_table]
        y_obs = [row.get("obs_cum_prob", row.get("prob_obt_acum")) for row in intervals_table]
        ax.scatter(x_obs, y_obs, color="#1f77b4", s=25, zorder=3, label="Frec. acumulada observada (intervalos)")

        # Hallar punto de máxima diferencia
        diff_key = "difference" if "difference" in intervals_table[0] else "diferencia"
        max_row = max(intervals_table, key=lambda r: r.get(diff_key, 0.0))
        x_dmax = max_row.get("end", max_row.get("final"))
        y_obs_dmax = max_row.get("obs_cum_prob", max_row.get("prob_obt_acum"))
        y_exp_dmax = max_row.get("exp_cum_prob", max_row.get("prob_esp_acum"))

        color_diff = "#2ca02c" if passed else "#d62728"
        ax.plot([x_dmax, x_dmax], [min(y_obs_dmax, y_exp_dmax), max(y_obs_dmax, y_exp_dmax)],
                color=color_diff, lw=3, marker="o", markersize=6,
                label=f"D_max = {d_max:.4f} (Crítico = {d_max_p:.4f})")

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.05)
    ax.set_title("Prueba de Kolmogorov-Smirnov - FEC vs Distribución Teórica")
    ax.set_xlabel("x")
    ax.set_ylabel("Probabilidad Acumulada F(x)")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    return fig


def obtener_figura(id_prueba: str, resultado: dict, secuencia: list[float] | None = None) -> Figure | None:
    """Devuelve la figura correspondiente a la prueba, generándola si no existe."""
    # Si el resultado ya tiene una figura embebida (ej. pruebas que la generen internamente)
    for llave in ("figure", "figura"):
        if isinstance(resultado.get(llave), Figure):
            return resultado[llave]

    # Generación en la vista según el tipo de prueba
    if id_prueba == "medias":
        return graficar_medias(resultado)
    elif id_prueba == "varianza":
        return graficar_varianza(resultado)
    elif id_prueba in ("ks", "kolmogorov_smirnov"):
        return graficar_ks(resultado, secuencia=secuencia)

    return None
