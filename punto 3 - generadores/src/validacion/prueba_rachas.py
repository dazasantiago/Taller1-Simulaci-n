import math

import matplotlib.pyplot as plt
from scipy import stats

SIGNIFICANCE_LEVEL = 0.05


def determinar_signos(sequence: list[float]) -> list[int]:
    signos = []
    for i in range(len(sequence) - 1):
        if sequence[i + 1] > sequence[i]:
            signos.append(1)
        elif sequence[i + 1] < sequence[i]:
            signos.append(-1)
    return signos


def contar_rachas(signos: list[int]) -> int:
    if len(signos) == 0:
        return 0

    num_rachas = 1
    for i in range(1, len(signos)):
        if signos[i] != signos[i - 1]:
            num_rachas += 1
    return num_rachas


def build_runs_plot(sequence: list[float], num_rachas: int):
    fig, ax = plt.subplots()
    ax.plot(range(len(sequence)), sequence, marker="o", linestyle="-", markersize=3)
    ax.set_xlabel("Índice")
    ax.set_ylabel("Valor")
    ax.set_title(f"Prueba de Rachas (rachas observadas: {num_rachas})")
    return fig


def runs_test(sequence: list[float]) -> dict:
    n = len(sequence)

    signos = determinar_signos(sequence)
    num_rachas = contar_rachas(signos)

    valor_esperado = (2 * n - 1) / 3
    varianza = (16 * n - 29) / 90
    statistic = (num_rachas - valor_esperado) / math.sqrt(varianza)

    critical_value = float(stats.norm.ppf(1 - SIGNIFICANCE_LEVEL / 2))
    passes_test = abs(statistic) <= critical_value

    figure = build_runs_plot(sequence, num_rachas)

    return {
        "statistic": statistic,
        "critical_value": critical_value,
        "num_runs": num_rachas,
        "passes_test": passes_test,
        "figure": figure,
    }
