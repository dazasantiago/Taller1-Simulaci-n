"""Adaptador de números pseudoaleatorios para la simulación Monte Carlo (EpiSim).

Conecta directamente el modelo SEIR del Punto 4 con el generador congruencial lineal
implementado desde cero en `punto 3 - generadores/src/generadores/congruencial.py`.
"""

from __future__ import annotations

import os
import sys

# Agregar la ruta de `src` del Punto 3 al path de Python para importar sus generadores
RUTA_PUNTO_3 = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "punto 3 - generadores", "src")
)
if RUTA_PUNTO_3 not in sys.path:
    sys.path.insert(0, RUTA_PUNTO_3)

from generadores.congruencial import congruencial_lineal
from generadores.distribuciones import uniforme_desde_enteros


class GeneradorMonteCarlo:
    """Adaptador de flujo estocástico que consume números de Punto 3 por lotes."""

    def __init__(
        self,
        semilla: int,
        a: int = 1664525,
        c: int = 1013904223,
        m: int = 2**32,
        lote: int = 5000,
    ):
        self.semilla = int(semilla) % m
        self.a = a
        self.c = c
        self.m = m
        self.lote = lote
        self.buffer: list[float] = []
        self.indice = 0

    def siguiente_uniforme(self) -> float:
        """Genera el siguiente número pseudoaleatorio uniforme en [0, 1)."""
        if self.indice >= len(self.buffer):
            enteros = congruencial_lineal(
                seed=self.semilla,
                a=self.a,
                c=self.c,
                m=self.m,
                count=self.lote,
            )
            self.semilla = enteros[-1]
            self.buffer = uniforme_desde_enteros(enteros, self.m)
            self.indice = 0
        valor = self.buffer[self.indice]
        self.indice += 1
        return valor
