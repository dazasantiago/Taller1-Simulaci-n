"""Prueba de rachas (corridas arriba/abajo) sobre una secuencia pseudoaleatoria."""
import math

import matplotlib.pyplot as plt
from scipy import stats

SIGNIFICANCE_LEVEL = 0.05


def runs_test(sequence: list[float]) -> dict:
    n = len(sequence)

    signs = []
    for i in range(n - 1):
        if sequence[i + 1] > sequence[i]:
            signs.append(1)
        elif sequence[i + 1] < sequence[i]:
            signs.append(-1)

    num_runs = 1
    for i in range(1, len(signs)):
        if signs[i] != signs[i - 1]:
            num_runs += 1

    expected = (2 * n - 1) / 3
    variance = (16 * n - 29) / 90
    statistic = (num_runs - expected) / math.sqrt(variance)

    critical_value = float(stats.norm.ppf(1 - SIGNIFICANCE_LEVEL / 2))
    p_value = float(2 * (1 - stats.norm.cdf(abs(statistic))))
    passes_test = abs(statistic) <= critical_value

    fig, ax = plt.subplots()
    ax.plot(range(n), sequence, marker="o", linestyle="-", markersize=3)
    ax.set_xlabel("Índice")
    ax.set_ylabel("Valor")
    ax.set_title(f"Prueba de Rachas (rachas observadas: {num_runs})")

    return {
        "statistic": statistic,
        "critical_value": critical_value,
        "p_value": p_value,
        "passes_test": passes_test,
        "figure": fig,
        "num_runs": num_runs,
    }
