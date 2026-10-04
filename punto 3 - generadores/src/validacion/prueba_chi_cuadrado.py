import matplotlib.pyplot as plt
from scipy import stats

SIGNIFICANCE_LEVEL = 0.05


def build_chi_square_table(intervals, observed_frequencies, expected_frequency):
    table = []
    for i in range(len(intervals)):
        start, end = intervals[i]
        observed = observed_frequencies[i]
        error = (observed - expected_frequency) ** 2 / expected_frequency
        table.append(
            {
                "interval": i + 1,
                "start": start,
                "end": end,
                "observed": observed,
                "expected": expected_frequency,
                "error": error,
            }
        )

    fig, ax = plt.subplots()
    positions = range(len(intervals))
    width = 0.4
    ax.bar(
        [p - width / 2 for p in positions],
        observed_frequencies,
        width=width,
        label="Observada",
    )
    ax.bar(
        [p + width / 2 for p in positions],
        [expected_frequency] * len(intervals),
        width=width,
        label="Esperada",
    )
    ax.set_xlabel("Intervalo")
    ax.set_ylabel("Frecuencia")
    ax.set_title("Prueba de Chi-cuadrado")
    ax.legend()

    return table, fig


def chi_square_test(sequence: list[float], n_intervals: int) -> dict:
    n = len(sequence)

    interval_width = 1 / n_intervals
    intervals = []
    for i in range(n_intervals):
        start = i * interval_width
        end = start + interval_width
        intervals.append((start, end))

    observed_frequencies = [0] * n_intervals
    for i in range(n_intervals):
        start, end = intervals[i]
        es_ultimo_intervalo = i == n_intervals - 1

        contador = 0
        for value in sequence:
            if es_ultimo_intervalo:
                if start <= value <= end:
                    contador += 1
            else:
                if start <= value < end:
                    contador += 1
        observed_frequencies[i] = contador

    expected_frequency = n / n_intervals
    statistic = 0
    for observed in observed_frequencies:
        error = (observed - expected_frequency) ** 2 / expected_frequency
        statistic += error

    number_of_columns = 2
    number_of_rows = n_intervals
    degrees_of_freedom = (number_of_columns - 1) * (number_of_rows - 1)

    critical_value = float(stats.chi2.ppf(1 - SIGNIFICANCE_LEVEL, degrees_of_freedom))
    passes_test = statistic <= critical_value

    table, figure = build_chi_square_table(intervals, observed_frequencies, expected_frequency)

    return {
        "statistic": statistic,
        "critical_value": critical_value,
        "degrees_of_freedom": degrees_of_freedom,
        "passes_test": passes_test,
        "table": table,
        "figure": figure,
    }
