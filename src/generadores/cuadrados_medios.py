"""Generador de números pseudoaleatorios: método de Cuadrados Medios.

Requisito estricto de la materia: NO usar `random`, `numpy.random` ni
ninguna otra librería de generación aleatoria del lenguaje. Solo
aritmética básica de Python (potencias, módulo, manejo de strings/ints
para extraer dígitos, etc.).
"""

from __future__ import annotations


def cuadrados_medios(semilla: int, n_digitos: int, cantidad: int) -> list[int]:
    """Genera una secuencia de números pseudoaleatorios con el método de Cuadrados Medios.

    Algoritmo esperado (a implementar):
        1. Tomar la semilla actual (inicialmente `semilla`) y elevarla al cuadrado.
        2. Rellenar el resultado con ceros a la izquierda hasta tener
           `2 * n_digitos` dígitos.
        3. Extraer los `n_digitos` dígitos centrales: ese valor es el
           siguiente número de la secuencia y también la nueva semilla
           para la siguiente iteración.
        4. Repetir el proceso hasta generar `cantidad` números.

    Args:
        semilla: Semilla inicial. Se espera que tenga exactamente
            `n_digitos` dígitos (entero positivo).
        n_digitos: Cantidad de dígitos que debe tener cada número
            generado (y la semilla).
        cantidad: Cantidad de números pseudoaleatorios a generar.

    Returns:
        list[int]: Lista de longitud `cantidad` con los números
        pseudoaleatorios generados, cada uno representable con
        `n_digitos` dígitos (valores SIN normalizar a [0, 1)). La
        normalización a distribución uniforme se realiza aparte en
        `generar_uniforme` (ver `distribuciones.py`), dividiendo cada
        valor entre 10 ** n_digitos.

    Raises:
        NotImplementedError: Función pendiente de implementación.

    TODO:
        - Validar que `semilla`, `n_digitos` y `cantidad` sean consistentes
          (ej. `semilla` >= 0, `n_digitos` > 0, `cantidad` > 0).
        - Implementar el relleno de ceros a la izquierda antes de extraer
          los dígitos centrales.
        - Definir qué hacer si la secuencia degenera a 0 (ciclo trivial):
          decidir si se documenta como limitación conocida o se corta la
          generación con una advertencia.
        - Documentar/registrar en `outputs/` (cuando se implemente el punto
          de entrada) el gráfico de dispersión o histograma que evidencie
          el comportamiento de la secuencia, si el taller lo pide.
    """
    # TODO: Implementar el método de Cuadrados Medios.
    raise NotImplementedError("cuadrados_medios: pendiente de implementación")
