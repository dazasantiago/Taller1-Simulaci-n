"""Punto de entrada / CLI del proyecto.

Implementar aqui:
    - Lectura de semillas desde archivo (.txt/.csv) o ingreso manual.
    - Seleccion de metodo(s) de generacion a ejecutar.
    - Seleccion de prueba(s) de validacion a ejecutar.
    - Menu interactivo o argumentos de linea de comandos (argparse) para
      disparar lo anterior.
"""

# ---------------------------------------------------------------------------
# Generadores congruenciales disponibles — descomentar para usar
# ---------------------------------------------------------------------------
#
# import os, sys
# sys.path.insert(0, os.path.dirname(__file__))
#
# from src.generadores.congruencial import (
#     linear_congruential,         # alias: congruencial_lineal
#     multiplicative_congruential, # alias: congruencial_multiplicativo
# )
#
# # --- Congruencial Lineal: X_{n+1} = (a * X_n + c) mod m ---
# # Parametros de referencia (periodo completo): a=1664525, c=1013904223, m=4294967296
# enteros_lcg = linear_congruential(
#     seed=12345, a=1664525, c=1013904223, m=4294967296, count=1000
# )
# uniformes_lcg = [x / 4294967296 for x in enteros_lcg]  # R_i en [0.0, 1.0)
#
# # --- Congruencial Multiplicativo: X_{n+1} = (a * X_n) mod m  (c = 0) ---
# # Parametros de referencia (periodo maximo, Park-Miller): a=16807, m=2147483647
# enteros_mcg = multiplicative_congruential(
#     seed=12345, a=16807, m=2147483647, count=1000
# )
# uniformes_mcg = [x / 2147483647 for x in enteros_mcg]  # R_i en [0.0, 1.0)
