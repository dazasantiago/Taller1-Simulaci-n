"""Prueba de bondad de ajuste Chi-cuadrado sobre una secuencia pseudoaleatoria."""
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
