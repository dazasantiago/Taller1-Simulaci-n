"""Prueba de varianza sobre una secuencia pseudoaleatoria (lógica pura)."""
import math
import pandas as pd
from scipy.stats import chi2

ALPHA_DEFAULT = 0.05


def variance_test(sequence: list[float], nivel_confianza: float = 0.95, alpha: float | None = None) -> dict:
    """Ejecuta la prueba de varianza sobre una secuencia de números pseudoaleatorios en [0, 1)."""
    n = len(sequence)
    if n <= 1:
        raise ValueError("Se requieren al menos 2 elementos para la prueba de varianza.")

    if alpha is not None:
        a = alpha
    elif nivel_confianza is not None:
        a = 1.0 - nivel_confianza
    else:
        a = ALPHA_DEFAULT

    mean = sum(sequence) / n
    variance = float(pd.Series(sequence).var())
    df = n - 1

    chi2_lower = float(chi2.ppf(a / 2, df))
    chi2_upper = float(chi2.ppf(1 - a / 2, df))

    lower_bound = chi2_lower / (12 * df)
    upper_bound = chi2_upper / (12 * df)
    theoretical_variance = 1.0 / 12.0

    passed_test = lower_bound < variance < upper_bound

    result = {
        "statistic": variance,
        "variance": variance,
        "mean": mean,
        "df": df,
        "n": n,
        "chi2_lower": chi2_lower,
        "chi2_upper": chi2_upper,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "theoretical_variance": theoretical_variance,
        "confidence_level": 1.0 - a,
        "alpha": a,
        "passed_test": passed_test,
        "passes_test": passed_test,
        # Spanish backward-compatibility keys
        "chi_inferior": chi2_lower,
        "chi_superior": chi2_upper,
        "limite_inferior": lower_bound,
        "limite_superior": upper_bound,
        "Promedio": mean,
        "promedio": mean,
        "varianza": variance,
        "pasa_prueba": passed_test,
    }
    return result


prueba_varianza = variance_test

