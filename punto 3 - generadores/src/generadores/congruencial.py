"""Generadores congruenciales de números pseudoaleatorios.

Expone:
    - linear_congruential(seed, a, c, m, count) -> list[int]
    - multiplicative_congruential(seed, a, m, count) -> list[int]

Devuelven enteros X_i en [0, m). La normalización a [0.0, 1.0)
ocurre en distribuciones.py. No se usa ninguna librería de aleatoriedad.
"""


def linear_congruential(
    seed: int,
    a: int,
    c: int,
    m: int,
    count: int,
) -> list:
    """Genera `count` enteros X_i en [0, m) con la recurrencia:
        X_{n+1} = (a * X_n + c) mod m   (Generador Congruencial Lineal)

    Parámetros
    ----------
    seed  : valor inicial X_0, en [0, m-1]
    a     : multiplicador, en [1, m-1]
    c     : incremento, en [0, m-1]
    m     : módulo, debe ser > 1
    count : cantidad de valores; retorna lista vacía si <= 0

    Lanza ValueError si algún parámetro está fuera de rango.
    """
    if m <= 1:
        raise ValueError(f"m debe ser mayor que 1 (recibido: m={m})")
    if not (1 <= a <= m - 1):
        raise ValueError(f"a debe estar en [1, m-1] (recibido: a={a}, m={m})")
    if not (0 <= c <= m - 1):
        raise ValueError(f"c debe estar en [0, m-1] (recibido: c={c}, m={m})")
    if not (0 <= seed <= m - 1):
        raise ValueError(
            f"seed debe estar en [0, m-1] (recibido: seed={seed}, m={m})"
        )

    if count <= 0:
        return []

    result = []
    x = seed
    for _ in range(count):
        x = (a * x + c) % m 
        result.append(x)

    return result


congruencial_lineal = linear_congruential


def multiplicative_congruential(
    seed: int,
    a: int,
    m: int,
    count: int,
) -> list:
    """Genera `count` enteros X_i en [0, m) con la recurrencia:
        X_{n+1} = (a * X_n) mod m   (Generador Congruencial Multiplicativo)

    Caso especial del lineal con c = 0. La semilla no puede ser
    multiplo de m: produciria una secuencia degenerada de ceros.

    Parámetros
    ----------
    seed  : valor inicial X_0, entero positivo, no múltiplo de m
    a     : multiplicador, >= 1
    m     : módulo, debe ser > 1
    count : cantidad de valores; retorna lista vacía si <= 0

    Lanza ValueError si algún parámetro está fuera de rango.
    """
    if m <= 1:
        raise ValueError(f"m debe ser mayor que 1 (recibido: m={m})")
    if a < 1:
        raise ValueError(f"a debe ser al menos 1 (recibido: a={a})")
    if seed <= 0:
        raise ValueError(
            f"seed debe ser un entero positivo (recibido: seed={seed})"
        )
    if seed % m == 0:
        raise ValueError(
            f"seed no puede ser multiplo de m "
            f"(seed={seed}, m={m}): produciria una secuencia degenerada de ceros"
        )

    if count <= 0:
        return []

    result = []
    x = seed
    for _ in range(count):
        x = (a * x) % m
        result.append(x)

    return result

congruencial_multiplicativo = multiplicative_congruential
