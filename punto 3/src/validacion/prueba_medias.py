"""Prueba de medias sobre una secuencia pseudoaleatoria."""
import math

from scipy.stats import norm

ALPHA = 0.05

#Prueba de medias
def means_test(sequence):
    n = len(sequence)
    mean = sum(sequence) / n
    z = norm.ppf(1 - (ALPHA / 2))

    lower_bound = 0.5 - z * math.sqrt(1 / (12 * n))
    upper_bound = 0.5 + z * math.sqrt(1 / (12 * n))

    passed_test = lower_bound < mean < upper_bound

    result = {
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "mean": mean,
        "passed_test": passed_test,
        # Spanish backward-compatibility keys
        "limite_inferior": lower_bound,
        "limite_superior": upper_bound,
        "promedio": mean,
        "pasa_prueba": passed_test,
    }
    return result


prueba_medias = means_test
