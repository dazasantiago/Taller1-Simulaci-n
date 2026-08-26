"""Distribuciones derivadas de los generadores propios (Uniforme y Normal).

Estas funciones NO generan aleatoriedad por su cuenta: se apoyan
únicamente en los generadores implementados en `cuadrados_medios.py` y
`congruencial.py`. Prohibido usar `random`, `numpy.random` o cualquier
otra librería de generación aleatoria del lenguaje.
"""

from __future__ import annotations

METODOS_BASE_VALIDOS = (
    "cuadrados_medios",
    "congruencial_lineal",
    "congruencial_multiplicativo",
    "congruencial_aditivo",
)
"""Nombres válidos para el parámetro `metodo` / `metodo_base`."""


def generar_uniforme(metodo: str, parametros: dict, cantidad: int) -> list[float]:
    """Genera una secuencia de números con distribución Uniforme(0, 1).

    Debe apoyarse en uno de los generadores propios (`cuadrados_medios`,
    `congruencial_lineal`, `congruencial_multiplicativo` o
    `congruencial_aditivo`) y normalizar su salida entera a valores
    reales en el intervalo [0, 1).

    Args:
        metodo: Nombre del generador base a usar. Debe ser uno de
            `METODOS_BASE_VALIDOS`
            (ej. "cuadrados_medios", "congruencial_lineal", ...).
        parametros: Diccionario con los parámetros específicos que
            requiere el generador elegido. Ejemplos esperados:
                - "cuadrados_medios": {"semilla": int, "n_digitos": int}
                - "congruencial_lineal": {"semilla": int, "a": int, "c": int, "m": int}
                - "congruencial_multiplicativo": {"semilla": int, "a": int, "m": int}
                - "congruencial_aditivo": {"semillas_iniciales": list[int], "m": int}
        cantidad: Cantidad de números Uniforme(0, 1) a generar.

    Returns:
        list[float]: Lista de longitud `cantidad` con valores en el
        rango [0, 1).

    Raises:
        NotImplementedError: Función pendiente de implementación.
        ValueError: (a implementar) si `metodo` no es reconocido o
            `parametros` no contiene las llaves requeridas por el método.

    TODO:
        - Despachar hacia la función generadora correspondiente según
          `metodo`, pasando `parametros` como argumentos.
        - Normalizar la salida entera del generador base a [0, 1)
          (ej. dividiendo entre 10**n_digitos o entre `m`, según el caso).
        - Validar `metodo` contra `METODOS_BASE_VALIDOS`.
    """
    # TODO: Implementar el despacho al generador base y la normalización a [0, 1).
    raise NotImplementedError("generar_uniforme: pendiente de implementación")


def generar_normal(metodo_base: str, parametros: dict, cantidad: int) -> list[float]:
    """Genera una secuencia de números con distribución Normal.

    Debe transformar números Uniforme(0, 1) —obtenidos vía
    `generar_uniforme` usando `metodo_base` como generador de base— en
    números con distribución Normal, usando una transformación como
    Box-Muller. NO debe usarse ninguna función de librería que genere
    valores normales directamente (ej. `numpy.random.normal`,
    `scipy.stats.norm.rvs`); `scipy`/`numpy` solo pueden usarse para
    operaciones matemáticas auxiliares (raíz, logaritmo, seno/coseno,
    manejo de arreglos), nunca para generar aleatoriedad.

    Transformación de referencia (Box-Muller, a implementar):
        Dadas dos uniformes independientes U1, U2 en (0, 1):
            Z0 = sqrt(-2 * ln(U1)) * cos(2 * pi * U2)
            Z1 = sqrt(-2 * ln(U1)) * sin(2 * pi * U2)
        Z0 y Z1 son dos valores independientes de una Normal(0, 1).

    Args:
        metodo_base: Nombre del generador base a usar para producir las
            uniformes subyacentes (ver `METODOS_BASE_VALIDOS`).
        parametros: Diccionario con los parámetros del generador base
            (mismo formato que en `generar_uniforme`). Opcionalmente
            puede incluir las llaves "media" (float, por defecto 0) y
            "desviacion" (float, por defecto 1) para desplazar/escalar
            el resultado estándar: X = media + desviacion * Z.
        cantidad: Cantidad de números con distribución Normal a generar.

    Returns:
        list[float]: Lista de longitud `cantidad` con valores distribuidos
        aproximadamente Normal(media, desviacion**2) (Normal estándar si
        no se especifican "media"/"desviacion" en `parametros`).

    Raises:
        NotImplementedError: Función pendiente de implementación.

    TODO:
        - Generar suficientes uniformes vía `generar_uniforme(metodo_base,
          parametros, ...)` (considerar que Box-Muller produce 2 valores
          normales por cada par de uniformes).
        - Implementar la transformación de Box-Muller.
        - Aplicar el desplazamiento/escala usando "media" y "desviacion"
          si están presentes en `parametros`.
        - Manejar el caso en que `cantidad` sea impar (Box-Muller genera
          pares de valores).
    """
    # TODO: Implementar la generación de números con distribución Normal (Box-Muller).
    raise NotImplementedError("generar_normal: pendiente de implementación")
