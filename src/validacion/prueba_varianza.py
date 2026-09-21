"""Prueba de varianza sobre una secuencia pseudoaleatoria."""
import pandas as pd
from scipy.stats import chi2

ALPHA = 0.05

def variance_test(sequence):
    n = len(sequence)
    mean = sum(sequence) / n
    variance = pd.Series(sequence).var()

    chi2_lower = chi2.ppf(ALPHA / 2, n - 1)
    chi2_upper = chi2.ppf(1 - ALPHA / 2, n - 1)

    lower_bound = chi2_lower / (12 * (n - 1))
    upper_bound = chi2_upper / (12 * (n - 1))

    passed_test = lower_bound < variance < upper_bound

    result = {
        "chi_lower": chi2_lower,
        "chi_upper": chi2_upper,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "mean": mean,
        "variance": variance,
        "passed_test": passed_test,
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
