"""Generadores de números pseudoaleatorios: métodos congruenciales.

Incluye los métodos:
    - Congruencial Lineal: X(n+1) = (a * X(n) + c) mod m
    - Congruencial Multiplicativo: X(n+1) = (a * X(n)) mod m
    - Congruencial Aditivo: X(n) = (X(n-1) + X(n-2) + ... + X(n-k)) mod m

Requisito estricto de la materia: NO usar `random`, `numpy.random` ni
ninguna otra librería de generación aleatoria del lenguaje. Solo
aritmética básica de Python.
"""

from __future__ import annotations


def congruencial_lineal(semilla: int, a: int, c: int, m: int, cantidad: int) -> list[int]:
    """Genera una secuencia de números con el método Congruencial Lineal.

    Fórmula esperada (a implementar):
        X(0) = semilla
        X(n+1) = (a * X(n) + c) mod m

    Args:
        semilla: Valor inicial X(0), con 0 <= semilla < m.
        a: Multiplicador de la fórmula congruencial.
        c: Incremento de la fórmula congruencial.
        m: Módulo de la fórmula congruencial (define el período máximo).
        cantidad: Cantidad de números pseudoaleatorios a generar.

    Returns:
        list[int]: Lista de longitud `cantidad` con los valores
        X(1), X(2), ..., X(cantidad) generados por la recurrencia
        (valores enteros en el rango [0, m), SIN normalizar a [0, 1)).

    Raises:
        NotImplementedError: Función pendiente de implementación.

    TODO:
        - Validar parámetros: m > 0, 0 <= semilla < m, a > 0, c >= 0.
        - Implementar la recurrencia y devolver la lista de valores.
        - (Opcional) Exponer utilidades para verificar las condiciones de
          Hull-Dobell que garantizan período completo, si el taller lo pide.
    """
    # TODO: Implementar el método Congruencial Lineal.
    raise NotImplementedError("congruencial_lineal: pendiente de implementación")


def congruencial_multiplicativo(semilla: int, a: int, m: int, cantidad: int) -> list[int]:
    """Genera una secuencia de números con el método Congruencial Multiplicativo.

    Fórmula esperada (a implementar):
        X(0) = semilla
        X(n+1) = (a * X(n)) mod m

    Args:
        semilla: Valor inicial X(0), con 0 < semilla < m (debe ser
            distinto de 0 para evitar degenerar la secuencia).
        a: Multiplicador de la fórmula congruencial.
        m: Módulo de la fórmula congruencial (define el período máximo).
        cantidad: Cantidad de números pseudoaleatorios a generar.

    Returns:
        list[int]: Lista de longitud `cantidad` con los valores
        X(1), X(2), ..., X(cantidad) generados por la recurrencia
        (valores enteros en el rango [0, m), SIN normalizar a [0, 1)).

    Raises:
        NotImplementedError: Función pendiente de implementación.

    TODO:
        - Validar parámetros: m > 0, 0 < semilla < m, a > 0.
        - Implementar la recurrencia y devolver la lista de valores.
    """
    # TODO: Implementar el método Congruencial Multiplicativo.
    raise NotImplementedError("congruencial_multiplicativo: pendiente de implementación")


def congruencial_aditivo(semillas_iniciales: list[int], m: int, cantidad: int) -> list[int]:
    """Genera una secuencia de números con el método Congruencial Aditivo.

    Fórmula esperada (a implementar), usando k = len(semillas_iniciales)
    valores iniciales:
        X(0), X(1), ..., X(k-1) = semillas_iniciales
        X(n) = (X(n-1) + X(n-2) + ... + X(n-k)) mod m,  para n >= k

    Args:
        semillas_iniciales: Lista con los k valores semilla iniciales
            (0 <= cada valor < m).
        m: Módulo de la fórmula congruencial.
        cantidad: Cantidad de números pseudoaleatorios NUEVOS a generar
            (es decir, valores X(k), X(k+1), ..., sin contar las semillas
            iniciales).

    Returns:
        list[int]: Lista de longitud `cantidad` con los nuevos valores
        generados por la recurrencia (valores enteros en el rango
        [0, m), SIN normalizar a [0, 1)).

    Raises:
        NotImplementedError: Función pendiente de implementación.

    TODO:
        - Validar que `semillas_iniciales` tenga al menos 2 elementos y
          que todos cumplan 0 <= valor < m.
        - Implementar la recurrencia manteniendo una ventana deslizante
          de los últimos k valores.
    """
    # TODO: Implementar el método Congruencial Aditivo.
    raise NotImplementedError("congruencial_aditivo: pendiente de implementación")
