"""Prueba de medias sobre una secuencia pseudoaleatoria (lógica pura)."""
import math
from scipy.stats import norm

ALPHA_DEFAULT = 0.05


def means_test(sequence: list[float], nivel_confianza: float = 0.95, alpha: float | None = None) -> dict:
    """Ejecuta la prueba de medias sobre una secuencia de números pseudoaleatorios en [0, 1)."""
    n = len(sequence)
    if n == 0:
        raise ValueError("La secuencia no puede estar vacía.")

    if alpha is not None:
        a = alpha
    elif nivel_confianza is not None:
        a = 1.0 - nivel_confianza
    else:
        a = ALPHA_DEFAULT

    mean = sum(sequence) / n
    z = float(norm.ppf(1 - (a / 2)))
    se = math.sqrt(1 / (12 * n))

    lower_bound = 0.5 - z * se
    upper_bound = 0.5 + z * se

    passed_test = lower_bound < mean < upper_bound

    result = {
        "statistic": mean,
        "mean": mean,
        "z_critical": z,
        "standard_error": se,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "confidence_level": 1.0 - a,
        "alpha": a,
        "n": n,
        "passed_test": passed_test,
        "passes_test": passed_test,
        # Spanish backward-compatibility keys
        "limite_inferior": lower_bound,
        "limite_superior": upper_bound,
        "promedio": mean,
        "pasa_prueba": passed_test,
    }
    return result


prueba_medias = means_test

