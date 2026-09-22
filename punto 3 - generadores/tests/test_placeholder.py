"""Prueba de humo (smoke test) del proyecto.

Verifica ÚNICAMENTE que todos los módulos del proyecto se puedan
importar sin errores. No prueba lógica de negocio: los generadores y
las pruebas estadísticas todavía no están implementados (son archivos
placeholder). Sirve como red de seguridad para detectar errores de
sintaxis o de importación mientras el equipo desarrolla el módulo.
"""

from __future__ import annotations

import importlib

import pytest

MODULOS = [
    "src",
    "src.generadores",
    "src.generadores.cuadrados_medios",
    "src.generadores.congruencial",
    "src.generadores.distribuciones",
    "src.validacion",
    "src.validacion.prueba_medias",
    "src.validacion.prueba_varianza",
    "src.validacion.prueba_chi_cuadrado",
    "src.validacion.prueba_kolmogorov_smirnov",
    "src.validacion.prueba_poker",
    "src.validacion.prueba_rachas",
    "main",
]


@pytest.mark.parametrize("nombre_modulo", MODULOS)
def test_modulo_importable(nombre_modulo: str) -> None:
    """Verifica que `nombre_modulo` se pueda importar sin lanzar excepciones."""
    importlib.import_module(nombre_modulo)
