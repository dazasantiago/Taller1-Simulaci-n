import matplotlib.pyplot as plt
from scipy import stats

SIGNIFICANCE_LEVEL = 0.05
HAND_SIZE = 5

CATEGORIES = [
    "Todos diferentes",
    "Un par",
    "Dos pares",
    "Tercia",
    "Full",
    "Poker",
    "Quintilla",
]

EXPECTED_PROBABILITIES = {
    "Todos diferentes": 0.3024,
    "Un par": 0.5040,
    "Dos pares": 0.1080,
    "Tercia": 0.0720,
    "Full": 0.0090,
    "Poker": 0.0045,
    "Quintilla": 0.0001,
}


def clasificar_mano(digitos: str) -> str:
    conteo_por_digito = [0] * 10
    for digito in digitos:
        conteo_por_digito[int(digito)] += 1

    repeticiones = []
    for conteo in conteo_por_digito:
        if conteo > 0:
            repeticiones.append(conteo)
    repeticiones.sort(reverse=True)

    if repeticiones == [1, 1, 1, 1, 1]:
        return "Todos diferentes"
    if repeticiones == [2, 1, 1, 1]:
        return "Un par"
    if repeticiones == [2, 2, 1]:
        return "Dos pares"
    if repeticiones == [3, 1, 1]:
        return "Tercia"
    if repeticiones == [3, 2]:
        return "Full"
    if repeticiones == [4, 1]:
        return "Poker"
    return "Quintilla"


def build_poker_table(observed_frequencies: dict, expected_frequencies: dict):
    table = []
    for categoria in CATEGORIES:
        observed = observed_frequencies[categoria]
        expected = expected_frequencies[categoria]
        error = (observed - expected) ** 2 / expected
        table.append(
            {
                "category": categoria,
                "observed": observed,
                "expected": expected,
                "error": error,
            }
        )

    observadas = []
    esperadas = []
    for categoria in CATEGORIES:
        observadas.append(observed_frequencies[categoria])
        esperadas.append(expected_frequencies[categoria])

    fig, ax = plt.subplots()
    positions = range(len(CATEGORIES))
    width = 0.4
    ax.bar(
        [p - width / 2 for p in positions],
        observadas,
        width=width,
        label="Observada",
    )
    ax.bar(
        [p + width / 2 for p in positions],
        esperadas,
        width=width,
        label="Esperada",
    )
    ax.set_xticks(list(positions))
    ax.set_xticklabels(CATEGORIES, rotation=45, ha="right")
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Frecuencia")
    ax.set_title("Prueba de Poker")
    ax.legend()
    fig.tight_layout()

    return table, fig


def poker_test(sequence: list[float]) -> dict:
    n = len(sequence)

    observed_frequencies = {}
    for categoria in CATEGORIES:
        observed_frequencies[categoria] = 0

    for value in sequence:
        digitos = f"{value:.{HAND_SIZE}f}".split(".")[1]
        categoria = clasificar_mano(digitos)
        observed_frequencies[categoria] += 1

    expected_frequencies = {}
    for categoria in CATEGORIES:
        expected_frequencies[categoria] = EXPECTED_PROBABILITIES[categoria] * n

    statistic = 0
    for categoria in CATEGORIES:
        observed = observed_frequencies[categoria]
        expected = expected_frequencies[categoria]
        error = (observed - expected) ** 2 / expected
        statistic += error

    number_of_columns = 2
    number_of_rows = len(CATEGORIES)
    degrees_of_freedom = (number_of_columns - 1) * (number_of_rows - 1)

    critical_value = float(stats.chi2.ppf(1 - SIGNIFICANCE_LEVEL, degrees_of_freedom))
    passes_test = statistic <= critical_value

    table, figure = build_poker_table(observed_frequencies, expected_frequencies)

    return {
        "statistic": statistic,
        "critical_value": critical_value,
        "degrees_of_freedom": degrees_of_freedom,
        "passes_test": passes_test,
        "table": table,
        "figure": figure,
    }
