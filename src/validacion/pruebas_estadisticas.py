"""Pruebas de validación estadística sobre secuencias pseudoaleatorias.

Implementar aquí:
    - prueba_medias(secuencia, nivel_confianza)
    - prueba_varianza(secuencia, nivel_confianza)
    - prueba_chi_cuadrado(secuencia, n_intervalos)
    - prueba_ks(secuencia)
    - prueba_poker(secuencia, tam_mano)
    - prueba_rachas(secuencia)
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
