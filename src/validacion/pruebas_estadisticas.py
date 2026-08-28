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
from scipy.stats import norm

#Prueba de medias
def prueba_medias(secuencia, nivel_confianza):
    promedio = sum(secuencia) / len(secuencia)
    constante = 1/2

    alfa = 1-nivel_confianza

    z = norm.ppf(1-alfa/2)

    Limite_inferior = constante - z *math.sqrt(1/(12*len(secuencia)))

    Limite_superior = constante + z *math.sqrt(1/(12*len(secuencia)))

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