"""Catálogo de generadores y pruebas que ofrece la interfaz.

Es el único punto de la app que toca `src/`. Cada función se busca por
nombre al vuelo y solo se ofrece en la interfaz si ya está implementada:
lo que sigue siendo un placeholder simplemente no aparece.

Contrato asumido de `src/` (ver docs/README.md):
    generar_uniforme(metodo, parametros, cantidad)
    generar_normal(metodo_base, parametros, cantidad)
donde `metodo` / `metodo_base` es el nombre de la función base
("cuadrados_medios", "congruencial_lineal", ...) y `parametros` es un dict
con los argumentos de esa función base (sin `cantidad`).
"""

from __future__ import annotations

import importlib
import inspect
from dataclasses import dataclass

import matplotlib.pyplot as plt


def cargar(modulo: str, nombre: str):
    """Devuelve `modulo.nombre` o None si el módulo/función aún no existe."""
    try:
        return getattr(importlib.import_module(modulo), nombre, None)
    except Exception:
        return None


@dataclass(frozen=True)
class Campo:
    """Parámetro numérico que la interfaz le pide al usuario."""

    nombre: str
    etiqueta: str
    defecto: int | float
    minimo: int | float | None = None
    maximo: int | float | None = None


# --------------------------------------------------------------------------
# Generadores
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Base:
    """Generador base: se invoca a través de generar_uniforme / generar_normal."""

    id: str  # nombre de la función en src y valor del argumento `metodo`
    etiqueta: str
    prefijo: str
    modulo: str
    campos: tuple[Campo, ...]
    vectorial: bool = False  # True: la "semilla" es una lista (aditivo)

    @property
    def clave_semilla(self) -> str:
        return "semillas_iniciales" if self.vectorial else "semilla"


BASES = (
    Base(
        "cuadrados_medios",
        "Cuadrados Medios",
        "CM",
        "src.generadores.cuadrados_medios",
        (Campo("n_digitos", "Número de dígitos (n_digitos)", 4, 1),),
    ),
    Base(
        "congruencial_lineal",
        "Congruencial Lineal",
        "LIN",
        "src.generadores.congruencial",
        (
            Campo("a", "Multiplicador (a)", 1103515245, 1),
            Campo("c", "Incremento (c)", 12345, 0),
            Campo("m", "Módulo (m)", 2**31, 2),  # ANSI C standard (ISO/IEC 9899:1990)
        ),
    ),
    Base(
        "congruencial_multiplicativo",
        "Congruencial Multiplicativo",
        "MUL",
        "src.generadores.congruencial",
        (
            Campo("a", "Multiplicador (a)", 48271, 1),
            Campo("m", "Módulo (m)", 2**31 - 1, 2),  # L'Ecuyer (1988), CACM
        ),
    ),
    Base(
        "congruencial_aditivo",
        "Congruencial Aditivo",
        "ADI",
        "src.generadores.congruencial",
        (Campo("m", "Módulo (m)", 2**31 - 1, 2),),
        vectorial=True,
    ),
)


@dataclass(frozen=True)
class Metodo:
    """Opción del selector de método de generación."""

    id: str
    etiqueta: str
    prefijo: str
    base: Base | None = None  # None en Normal: la base se elige aparte
    normal: bool = False


def bases_disponibles() -> list[Base]:
    if cargar("src.generadores.distribuciones", "generar_uniforme") is None:
        return []
    return [b for b in BASES if cargar(b.modulo, b.id) is not None]


def metodos_disponibles() -> list[Metodo]:
    bases = bases_disponibles()
    metodos = [Metodo(b.id, b.etiqueta, b.prefijo, base=b) for b in bases]
    if bases and cargar("src.generadores.distribuciones", "generar_normal") is not None:
        metodos.append(Metodo("normal", "Normal (Box-Muller)", "NOR", normal=True))
    return metodos


def parametros_base(base: Base, campos: dict, semilla: int | list[int]) -> dict:
    """Arma el dict `parametros` que reciben generar_uniforme / generar_normal."""
    return {base.clave_semilla: semilla, **campos}


def generar(metodo: Metodo, base: Base, parametros: dict, cantidad: int) -> list[float]:
    if metodo.normal:
        funcion = cargar("src.generadores.distribuciones", "generar_normal")
    else:
        funcion = cargar("src.generadores.distribuciones", "generar_uniforme")
    return [float(v) for v in funcion(base.id, parametros, cantidad)]


# --------------------------------------------------------------------------
# Pruebas de validación
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Prueba:
    id: str
    etiqueta: str
    modulo: str
    funcion: str
    campos: tuple[Campo, ...] = ()


PRUEBAS = (
    Prueba(
        "medias",
        "Prueba de medias",
        "src.validacion.prueba_medias",
        "prueba_medias",
        (Campo("nivel_confianza", "Nivel de confianza", 0.95, 0.5, 0.999),),
    ),
    Prueba(
        "varianza",
        "Prueba de varianza",
        "src.validacion.prueba_varianza",
        "prueba_varianza",
        (Campo("nivel_confianza", "Nivel de confianza", 0.95, 0.5, 0.999),),
    ),
    Prueba(
        "chi_cuadrado",
        "Prueba Chi-cuadrado",
        "src.validacion.prueba_chi_cuadrado",
        "chi_square_test",
        (Campo("n_intervals", "Número de intervalos", 10, 2, 1000),),
    ),
    Prueba(
        "ks",
        "Prueba de Kolmogorov-Smirnov",
        "src.validacion.prueba_kolmogorov_smirnov",
        "prueba_ks",
    ),
    Prueba(
        "poker",
        "Prueba de Póker",
        "src.validacion.prueba_poker",
        "poker_test",
        (Campo("hand_size", "Tamaño de la mano (dígitos)", 5, 2, 8),),
    ),
    Prueba(
        "rachas",
        "Prueba de rachas",
        "src.validacion.prueba_rachas",
        "runs_test",
    ),
)


def pruebas_disponibles() -> list[Prueba]:
    return [p for p in PRUEBAS if cargar(p.modulo, p.funcion) is not None]


def campos_aceptados(prueba: Prueba) -> tuple[Campo, ...]:
    """Campos de la prueba que la función implementada realmente recibe."""
    funcion = cargar(prueba.modulo, prueba.funcion)
    aceptados = inspect.signature(funcion).parameters
    return tuple(c for c in prueba.campos if c.nombre in aceptados)


def ejecutar_prueba(prueba: Prueba, valores: list[float], parametros: dict) -> dict:
    """Corre la prueba; ante un fallo devuelve {"error": ...} en vez de propagarlo."""
    funcion = cargar(prueba.modulo, prueba.funcion)
    permitidos = {c.nombre for c in campos_aceptados(prueba)}
    kwargs = {k: v for k, v in parametros.items() if k in permitidos}
    try:
        return funcion(list(valores), **kwargs)
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}
    finally:
        # Las pruebas crean figuras con pyplot; se liberan del registro global
        # (el objeto Figure devuelto en el dict sigue siendo válido).
        plt.close("all")
