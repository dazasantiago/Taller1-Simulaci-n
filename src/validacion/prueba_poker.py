"""Prueba de póker sobre una secuencia pseudoaleatoria."""
import math
from collections import Counter

import matplotlib.pyplot as plt
from scipy import stats

SIGNIFICANCE_LEVEL = 0.05


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
