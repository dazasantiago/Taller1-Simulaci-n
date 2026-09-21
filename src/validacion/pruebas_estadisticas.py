"""Pruebas de validación estadística sobre secuencias pseudoaleatorias.

Implementar aquí:
    - prueba_medias(secuencia, nivel_confianza)
    - prueba_varianza(secuencia, nivel_confianza)
    - chi_square_test(sequence, n_intervals)
    - prueba_ks(secuencia)
    - poker_test(sequence, hand_size)
    - runs_test(sequence)
"""
import math
import pandas as pd
from scipy.stats import norm
from scipy.stats import chi2

#Prueba de medias
def prueba_medias(secuencia):
    alfa = 0.05
    n = len(secuencia)
    promedio = sum(secuencia) / n
    z = norm.ppf(1-(alfa/2))

    Limite_inferior = 0.5 - z *math.sqrt(1/(12*len(secuencia)))
    Limite_superior = 0.5 + z *math.sqrt(1/(12*len(secuencia)))

    if Limite_inferior < promedio < Limite_superior:
        aprovado = True
    else:
        aprovado = False

    resultado = {
        "limite_inferior": Limite_inferior,
        "limite_superior": Limite_superior,
        "promedio": promedio,
        "pasa_prueba": aprovado,
    }
    return resultado

#Prueba de Varianzas
def prueba_varianza(secuencia):
    alfa = 0.05
    n = len(secuencia)
    promedio = sum(secuencia) / n
    varianza = pd.Series(secuencia).var()

    chi2_inferior = chi2.ppf(alfa / 2, n - 1)
    chi2_superior = chi2.ppf(1-alfa / 2, n - 1)

    Limite_inferior = chi2_inferior / (12 * (n - 1))
    Limite_superior = chi2_superior / (12 * (n - 1))

    if Limite_inferior < varianza < Limite_superior:
        aprovado = True
    else:
        aprovado = False

    resultado = {
        "chi_inferior": chi2_inferior,
        "chi_superior": chi2_superior,
        "limite_inferior": Limite_inferior,
        "limite_superior": Limite_superior,
        "Promedio": promedio,
        "varianza": varianza,
        "pasa_prueba": aprovado,
    }
    return resultado

import math
from collections import Counter

import matplotlib.pyplot as plt
from scipy import stats

SIGNIFICANCE_LEVEL = 0.05


def chi_square_test(sequence: list[float], n_intervals: int) -> dict:
    n = len(sequence)
    expected = n / n_intervals

    observed_frequencies = [0] * n_intervals
    for value in sequence:
        interval = min(int(value * n_intervals), n_intervals - 1)
        observed_frequencies[interval] += 1

    expected_frequencies = [expected] * n_intervals

    statistic = sum(
        (observed - expected) ** 2 / expected for observed in observed_frequencies
    )

    degrees_of_freedom = n_intervals - 1
    critical_value = float(stats.chi2.ppf(1 - SIGNIFICANCE_LEVEL, degrees_of_freedom))
    p_value = float(stats.chi2.sf(statistic, degrees_of_freedom))
    passes_test = statistic <= critical_value

    fig, ax = plt.subplots()
    positions = range(n_intervals)
    width = 0.4
    ax.bar(
        [p - width / 2 for p in positions],
        observed_frequencies,
        width=width,
        label="Observada",
    )
    ax.bar(
        [p + width / 2 for p in positions],
        expected_frequencies,
        width=width,
        label="Esperada",
    )
    ax.set_xlabel("Intervalo")
    ax.set_ylabel("Frecuencia")
    ax.set_title("Prueba de Chi-cuadrado")
    ax.legend()

    return {
        "statistic": statistic,
        "critical_value": critical_value,
        "p_value": p_value,
        "passes_test": passes_test,
        "figure": fig,
        "observed_frequencies": observed_frequencies,
        "expected_frequencies": expected_frequencies,
    }


def _partitions(n: int, max_part: int | None = None):
    """Generate the integer partitions of n as descending tuples."""
    if max_part is None:
        max_part = n
    if n == 0:
        yield ()
        return
    for first in range(min(n, max_part), 0, -1):
        for rest in _partitions(n - first, first):
            yield (first,) + rest


def _partition_label(partition: tuple[int, ...]) -> str:
    return "-".join(str(size) for size in partition)


def _partition_probability(partition: tuple[int, ...], hand_size: int) -> float:
    """Probability of drawing a hand with this digit-repetition shape.

    Combines: ways to group the `hand_size` positions according to the
    partition's group sizes, with ways to assign distinct digits (0-9)
    to each group.
    """
    k = len(partition)
    denominator = 1
    for group_size in partition:
        denominator *= math.factorial(group_size)
    for count in Counter(partition).values():
        denominator *= math.factorial(count)
    grouping_ways = math.factorial(hand_size) // denominator
    digit_assignment_ways = math.perm(10, k)
    return grouping_ways * digit_assignment_ways / 10**hand_size


def poker_test(sequence: list[float], hand_size: int) -> dict:
    n = len(sequence)
    partitions = list(_partitions(hand_size))

    category_frequencies = {_partition_label(p): 0 for p in partitions}
    for value in sequence:
        digits = f"{value:.{hand_size}f}".split(".")[1]
        shape = tuple(sorted(Counter(digits).values(), reverse=True))
        category_frequencies[_partition_label(shape)] += 1

    expected_frequencies = {
        _partition_label(p): _partition_probability(p, hand_size) * n
        for p in partitions
    }

    statistic = sum(
        (category_frequencies[label] - expected) ** 2 / expected
        for label, expected in expected_frequencies.items()
        if expected > 0
    )

    degrees_of_freedom = len(partitions) - 1
    critical_value = float(stats.chi2.ppf(1 - SIGNIFICANCE_LEVEL, degrees_of_freedom))
    p_value = float(stats.chi2.sf(statistic, degrees_of_freedom))
    passes_test = statistic <= critical_value

    fig, ax = plt.subplots()
    labels = list(category_frequencies.keys())
    positions = range(len(labels))
    width = 0.4
    ax.bar(
        [p - width / 2 for p in positions],
        [category_frequencies[label] for label in labels],
        width=width,
        label="Observada",
    )
    ax.bar(
        [p + width / 2 for p in positions],
        [expected_frequencies[label] for label in labels],
        width=width,
        label="Esperada",
    )
    ax.set_xticks(list(positions))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_xlabel("Categoría (tamaños de grupos de dígitos repetidos)")
    ax.set_ylabel("Frecuencia")
    ax.set_title("Prueba de Poker")
    ax.legend()
    fig.tight_layout()

    return {
        "statistic": statistic,
        "critical_value": critical_value,
        "p_value": p_value,
        "passes_test": passes_test,
        "figure": fig,
        "category_frequencies": category_frequencies,
    }


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
