"""Distribuciones Uniforme y Normal a partir de listas enteros 

Este módulo convierte los enteros Xi producidos por los generadores de

- cuadrados medios
- congruencial lineal
- congruencial multiplicativo

en valores uniformes Ri en [0, 1), y a partir de ellos genera valores
normales con box muller.

Contenido
---------
1. Conversión a uniforme:
   - uniforme_desde_enteros(enteros, m)
   - uniforme_rango_desde_enteros(enteros, m, a, b)

2. Conversión a normal vía transformación de Box-Muller:
   - normal_box_muller(uniformes, mu, sigma)

3. Utilidades de validación:
   - resumen_estadistico(valores)
   - histograma_frecuencias(valores, n_bins, a, b)

Convenciones
------------
- `Xi` : entero producido por el generador, en [0, m).
- `m`  : módulo del generador (ej: 2**32 para LCG, 10**n_digitos para
         cuadrados medios).
- `Ri` : valor uniforme estándar en [0, 1).
- `Ui` : valor uniforme en un rango [a, b).
- `Zi` : valor normal estándar N(0, 1).
"""

import math

def uniforme_desde_enteros(enteros, m):
    """Convierte enteros Xi en [0, m) a uniformes Ri en [0, 1).

    Fórmula:
        Ri = Xi / m

    Parámetros
    ----------
    enteros : list[int] o iterable de int
        Valores enteros producidos por un generador. Deben estar en [0, m).
    m : int
        Módulo del generador. Todos los enteros deben ser < m.

    Retorna
    -------
    list[float]
        Valores uniformes Ri en [0, 1).

    Lanza
    -----
    ValueError
        Si m <= 0 o si algún entero está fuera de [0, m).
    """
    if m <= 0:
        raise ValueError("m debe ser positivo.")
    salida = []
    for x in enteros:
        if x < 0 or x >= m:
            raise ValueError(f"Entero {x} fuera de [0, {m}).")
        salida.append(x / m)
    return salida


def uniforme_rango_desde_enteros(enteros, m, a, b):
    """Convierte enteros Xi en [0, m) a uniformes en un rango [a, b).

    Parámetros
    ----------
    enteros : list[int] 
        Valores enteros producidos por un generador.
    m : int
        Módulo del generador.
    a : float
        Límite inferior del intervalo.
    b : float
        Límite superior del intervalo. Debe ser > a.

    Retorna
    -------
    list[float] Valores uniformes Ui en [a, b).

    Lanza
    -----
    ValueError
        Si b <= a o si algún entero está fuera de [0, m).
    """
    if b <= a:
        raise ValueError("Se requiere b > a.")
    u = uniforme_desde_enteros(enteros, m)
    return [a + (b - a) * ui for ui in u]


def normal_box_muller(uniformes, mu=0.0, sigma=1.0):
    """Genera normales a partir de los numeros uniformes usando Box-Muller.

    Parámetros
    ----------
    uniformes : list[float] Valores uniformes en [0, 1).
        
    mu : float, opcional (default=0.0)
    
    sigma : float, opcional (default=1.0)
        Desviación estándar. Debe ser > 0.

    Retorna
    -------
    list[float]
        Valores normales N(mu, sigma²). La longitud es:
          - len(uniformes)      si es par
          - len(uniformes) - 1  si es impar

    Lanza
    -----
    ValueError
        Si sigma <= 0.
    """
    if sigma <= 0:
        raise ValueError("sigma debe ser > 0.")
    salida = []
    n = len(uniformes) - (len(uniformes) % 2)
    for i in range(0, n, 2):
        u1, u2 = uniformes[i], uniformes[i + 1]
        if u1 <= 0:
            u1 = 1e-12
        r = math.sqrt(-2 * math.log(u1))
        theta = 2 * math.pi * u2
        z1 = r * math.cos(theta)
        z2 = r * math.sin(theta)
        salida.append(mu + sigma * z1)
        salida.append(mu + sigma * z2)
    return salida


def resumen_estadistico(valores):
    """Devuelve media, varianza y desviación estándar de una lista.

    Parámetros
    ----------
    valores : list[float]

    Retorna
    -------
    dict
        Claves: 'n', 'media', 'varianza', 'desviacion'.
    """
    n = len(valores)
    if n == 0:
        return {"n": 0, "media": None, "varianza": None, "desviacion": None}
    media = sum(valores) / n
    if n == 1:
        return {"n": 1, "media": media, "varianza": 0.0, "desviacion": 0.0}
    var = sum((x - media) ** 2 for x in valores) / (n - 1)
    return {
        "n": n,
        "media": media,
        "varianza": var,
        "desviacion": math.sqrt(var),
    }


def histograma_frecuencias(valores, n_bins=10, a=0.0, b=1.0):
    """Calcula las frecuencias de un histograma para valores en [a, b).

    Parámetros
    ----------
    valores : list[float]
    n_bins : int, opcional (default=10)
        Número de intervalos.
    a : float, opcional (default=0.0)
        Límite inferior del rango.
    b : float, opcional (default=1.0)
        Límite superior del rango.

    Retorna
    -------
    dict
        Claves:
          - 'bins'       : lista de tuplas (inicio, fin) de cada bin.
          - 'frecuencias': lista de conteos por bin.
          - 'esperado'   : conteo esperado por bin si fuera uniforme.

    """
    if n_bins <= 0:
        raise ValueError("n_bins debe ser positivo.")
    if b <= a:
        raise ValueError("Se requiere b > a.")
    ancho = (b - a) / n_bins
    bins = [(a + i * ancho, a + (i + 1) * ancho) for i in range(n_bins)]
    frecuencias = [0] * n_bins
    for v in valores:
        if v < a or v >= b:
            continue
        idx = int((v - a) / ancho)
        if idx == n_bins:
            idx = n_bins - 1
        frecuencias[idx] += 1
    esperado = len(valores) / n_bins
    return {"bins": bins, "frecuencias": frecuencias, "esperado": esperado}


def generar_uniforme(metodo: str, parametros: dict, cantidad: int) -> list[float]:
    """Genera una lista de `cantidad` números uniformes en [0, 1) a partir de un generador base."""
    if cantidad <= 0:
        return []

    if metodo == "cuadrados_medios":
        try:
            from src.generadores.cuadrados_medios import cuadrados_medios
        except ImportError:
            from generadores.cuadrados_medios import cuadrados_medios
        semilla = parametros["semilla"]
        n_digitos = parametros.get("n_digitos", 4)
        m = 10 ** n_digitos
        enteros = cuadrados_medios(semilla=semilla, n_digitos=n_digitos, cantidad=cantidad)
        return uniforme_desde_enteros(enteros, m)

    elif metodo == "congruencial_lineal":
        try:
            from src.generadores.congruencial import congruencial_lineal
        except ImportError:
            from generadores.congruencial import congruencial_lineal
        semilla = parametros.get("semilla", parametros.get("seed", 1))
        a = parametros["a"]
        c = parametros["c"]
        m = parametros["m"]
        enteros = congruencial_lineal(seed=semilla, a=a, c=c, m=m, count=cantidad)
        return uniforme_desde_enteros(enteros, m)

    elif metodo == "congruencial_multiplicativo":
        try:
            from src.generadores.congruencial import congruencial_multiplicativo
        except ImportError:
            from generadores.congruencial import congruencial_multiplicativo
        semilla = parametros.get("semilla", parametros.get("seed", 1))
        a = parametros["a"]
        m = parametros["m"]
        enteros = congruencial_multiplicativo(seed=semilla, a=a, m=m, count=cantidad)
        return uniforme_desde_enteros(enteros, m)

    else:
        raise ValueError(f"Método '{metodo}' no reconocido o no soportado.")


def generar_normal(metodo_base: str, parametros: dict, cantidad: int, mu: float = 0.0, sigma: float = 1.0) -> list[float]:
    """Genera una lista de `cantidad` números normales N(mu, sigma²) vía Box-Muller."""
    if cantidad <= 0:
        return []
    n_necesarios = cantidad + (cantidad % 2)
    uniformes = generar_uniforme(metodo_base, parametros, n_necesarios)
    normales = normal_box_muller(uniformes, mu=mu, sigma=sigma)
    return normales[:cantidad]