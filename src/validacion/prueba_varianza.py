"""Prueba de varianza sobre una secuencia pseudoaleatoria."""
import pandas as pd
from scipy.stats import chi2


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
