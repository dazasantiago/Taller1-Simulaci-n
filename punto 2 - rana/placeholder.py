"""Simulación de caminata en 1D.

Descripción general
-------------------
- Partida desde el origen
- Idéntica probabilidad (0.5 cada uno).

Estrategia de simulación 
---------------------------------------------------
La caminata se simula por LOTES encadenados. El estado que pasa de un lote
al siguiente es:
    1. Posición final del lote anterior  -> posición inicial del siguiente.
    2. Valor de la secuencia en donde quedo -> continúa la secuencia pseudoaleatoria.
    3. Flag que marca si ya pasó por el origen      -> se arrastra entre lotes.


Arquitectura
------------
- Con el modulo de generadores se producen enteros Xi.
- Con el modulo de distribuciones se convierten a uniformes Ri en [0, 1).
- Este modulo usa los Ri para decidir cada paso (+1 si Ri < 0.5, -1 si no).

Convenciones
------------
Convenciones y notación
-----------------------
Variables de la caminata:
- `pos`       : posición actual de la rana en la recta.
                Se actualiza al final de cada lote y es la entrada del
                siguiente lote. Al inicio vale 0.
- `paso`      : cada movimiento individual (+1 o -1).
- `tray`      : trayectoria acumulada dentro de un lote. Es un array
                con la posición después de cada paso del lote.
- `visito`    : booleano que indica si la rana ya tocó el origen (pos=0)
                en algún momento hasta el lote actual. Se arrastra entre
                lotes.
- `marca`     : número de paso específico (default 1000) en el que se
                registra la posición y el flag `visito`, para analizar
                el retorno al origen.

Cantidades:
- `n_pasos`   : número total de pasos por réplica.
- `n_rep`     : número de réplicas independientes.
- `n_lote`    : número de pasos a dar por lote. La simulación se
                divide en lotes de este tamaño.
- `hecho`     : pasos ya completados hasta el momento (contador interno).
- `tam`       : tamaño del lote actual. Es min(n_lote, n_pasos - hecho),
                porque el último lote puede ser parcial.
- `m`         : módulo del generador (ej: 2**32). Se usa para normalizar
                los enteros Xi a uniformes Ri.

Variables aleatorias:
- `Xi`        : entero producido por el generador del equipo, en [0, m).
- `Ri`        : valor uniforme en [0, 1) obtenido como Ri = Xi / m. La
                caminata lo usa para decidir el paso: Ri < 0.5 -> +1,
                Ri >= 0.5 -> -1.
- `sigma`     : desviación estándar teórica de la posición final tras
                n_pasos pasos. Vale sqrt(n_pasos) por el Teorema Central
                del Límite. Se usa como referencia en `resumir`.
"""

import argparse
import csv
import math
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Agregar la ruta del Punto 3 para importar el módulo de distribuciones.
RUTA_PUNTO_3 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "punto 3 - generadores", "src"
)
sys.path.insert(0, RUTA_PUNTO_3)

from generadores.distribuciones import uniforme_desde_enteros


# ============================================================================
# 1. WRAPPER DE GENERADORES
# ============================================================================
class GeneradorConectado:
    """
    La caminata necesita pedir lotes de números uniformes en [0, 1).
    El generador del equipo produce enteros Xi, y el módulo de
    distribuciones los convierte a uniformes Ri.

    Este wrapper:
        1. Llama al generador con los parámetros guardados.
        2. Convierte los enteros a uniformes usando `distribuciones`.
        3. Encadena el estado: el último entero generado se reusa como
           semilla en la próxima llamada.

    Parámetros del constructor
    --------------------------
    funcion : Función generadora del equipo. Firma asumida:
            funcion(semilla, ..., cantidad) -> list[int]
    m : int
        Módulo del generador. Se usa para normalizar Xi -> Ri.
    **parametros : dict
        Parámetros específicos del generador (semilla, a, c, etc.). 
        Se ingresan con nombre=valor.


    Atributos internos
    ------------------
    self.funcion : callable
        Generador envuelto.
    self.m : int
        Módulo del generador.
    self.parametros : dict
        Parámetros del generador. `self.parametros['semilla']` se
        actualiza en cada lote con el último entero generado.
    """

    def __init__(self, funcion, m, **parametros):
        if "semilla" not in parametros:
            raise ValueError("Se requiere 'semilla' en los parámetros.")
        self.funcion = funcion
        self.m = m
        self.parametros = parametros

    def siguiente_lote(self, cantidad):
        """Genera `cantidad` uniformes en [0, 1) y encadena el estado.

        Parámetros
        ----------
        cantidad : int
            Número de valores a generar en este lote.

        Retorna
        -------
        list[float]
            Valores uniformes Ri en [0, 1).
        """
        # 1. Llamar al generador del equipo
        enteros = self.funcion(cantidad=cantidad, **self.parametros)

        # 2. Encadenar el estado: el último entero se vuelve la nueva semilla
        self.parametros["semilla"] = enteros[-1]

        # 3. Convertir a uniformes con el módulo de distribuciones
        return uniforme_desde_enteros(enteros, self.m)


# ============================================================================
# 2. PUNTO DE CONFIGURACIÓN
# ============================================================================
# AQUÍ se cambia el generador cuando esté listo el del equipo.
#
# Ejemplo con congruencial lineal (firma asumida):
#   from generadores.congruencial import congruencial_lineal
#   def crear_generador(semilla):
#       return GeneradorConectado(
#           funcion=congruencial_lineal,
#           m=2**32,
#           semilla=semilla,
#           a=1664525,
#           c=1013904223,
#           m=2**32,
#       )
#
# Mientras tanto, se deja una función que lanza error claro.
# ----------------------------------------------------------------------------

def crear_generador(semilla):
    """Crea un generador conectado a la caminata.

    ÚNICO punto a modificar cuando lleguen los generadores del equipo.

    Parámetros
    ----------
    semilla : int
        Semilla inicial del generador.

    Retorna
    -------
    GeneradorConectado
        Objeto con método `.siguiente_lote(cantidad)`.
    """
    # ========================================================================
    # DESCOMENTAR Y AJUSTAR CUANDO LLEGUEN LOS GENERADORES DEL EQUIPO
    # ========================================================================
    # from generadores.congruencial import congruencial_lineal
    # return GeneradorConectado(
    #     funcion=congruencial_lineal,
    #     m=2**32,
    #     semilla=semilla,
    #     a=1664525,
    #     c=1013904223,
    #     m=2**32,
    # )
    raise NotImplementedError(
        "Falta conectar el generador del equipo. Editar `crear_generador`."
    )


# ============================================================================
# 3. SEMILLAS
# ============================================================================
def semillas_desde_base(semilla_base, n_rep):
    """Genera `n_rep` semillas separadas a partir de una semilla base.

    Parámetros
    ----------
    semilla_base : int
        Semilla de la primera réplica.
    n_rep : int
        Número de réplicas.

    Retorna
    -------
    list[int]
        Lista de `n_rep` enteros en [0, 2^32).
    """
    return [(semilla_base + i * 2654435761) % 2**32 for i in range(n_rep)]


def semillas_desde_archivo(ruta, n_rep):
    """Lee semillas desde un archivo .txt o .csv.

    Parámetros
    ----------
    ruta : str
        Ruta al archivo.
    n_rep : int
        Número mínimo de semillas requeridas.

    Retorna
    -------
    list[int]
        Primeras `n_rep` semillas del archivo.

    Lanza
    -----
    ValueError
        Si el archivo tiene menos de `n_rep` semillas.
    """
    with open(ruta, encoding="utf-8") as f:
        texto = f.read().replace(",", " ").replace(";", " ")
    semillas = [int(t) for t in texto.split()]
    if len(semillas) < n_rep:
        raise ValueError(f"El archivo tiene {len(semillas)} semillas y se piden {n_rep}.")
    return semillas[:n_rep]


# ============================================================================
# 4. SIMULACIÓN POR LOTES
# ============================================================================
def avanzar_lote(gen, pos, visito, n_lote, paso_inicio, marca=1000):
    """Avanza `n_lote` pasos de UNA réplica partiendo del estado recibido.

    Parámetros
    ----------
    gen : GeneradorConectado
        Generador con método `.siguiente_lote(cantidad)`.
    pos : int
        Posición al inicio del lote.
    visito : bool
        True si la rana ya pasó por el origen en lotes anteriores.
    n_lote : int
        Pasos a simular en este lote.
    paso_inicio : int
        Pasos ya completados antes de este lote.
    marca : int, opcional (default=1000)
        Paso en el que se registra posición y visito.

    Retorna
    -------
    nueva_pos : int
    nuevo_visito : bool
    registro : tuple(int, bool) | None
    """
    u = np.asarray(gen.siguiente_lote(n_lote))
    pasos = np.where(u < 0.5, 1, -1)
    tray = pos + np.cumsum(pasos, dtype=np.int64)

    registro = None
    if paso_inicio < marca <= paso_inicio + n_lote:
        idx = marca - paso_inicio - 1
        registro = (int(tray[idx]),
                    bool(visito or (tray[: idx + 1] == 0).any()))

    return int(tray[-1]), bool(visito or (tray == 0).any()), registro


def simular_replica(semilla, n_pasos, n_lote, marca=1000, guardar_tray=False):
    """Simula UNA réplica completa de la caminata 1D.

    Parámetros
    ----------
    semilla : int
    n_pasos : int
    n_lote : int
    marca : int, opcional (default=1000)
    guardar_tray : bool, opcional (default=False)

    Retorna
    -------
    pos : int
    reg : tuple(int, bool) | None
    trayectoria : list[int] | None
    """
    gen = crear_generador(semilla)
    pos, visito, hecho, reg = 0, False, 0, None
    trayectoria = [] if guardar_tray else None

    while hecho < n_pasos:
        tam = min(n_lote, n_pasos - hecho)
        pos, visito, r = avanzar_lote(gen, pos, visito, tam, hecho, marca)
        if r is not None:
            reg = r
        hecho += tam
        if guardar_tray:
            trayectoria.append(pos)

    return pos, reg, trayectoria


def simular(semillas, n_pasos, n_lote, marca=1000):
    """Corre todas las réplicas independientes.

    Parámetros
    ----------
    semillas : list[int]
    n_pasos : int
    n_lote : int
    marca : int, opcional (default=1000)

    Retorna
    -------
    finales : np.ndarray[int]
    pos_marca : np.ndarray[int]
    visito_marca : np.ndarray[bool]
    """
    finales, pos_marca, visito_marca = [], [], []
    for s in semillas:
        pos, reg, _ = simular_replica(s, n_pasos, n_lote, marca)
        finales.append(pos)
        if reg is not None:
            pos_marca.append(reg[0])
            visito_marca.append(reg[1])
    return np.array(finales), np.array(pos_marca), np.array(visito_marca)


# ============================================================================
# 5. VERIFICACIÓN DE EQUIVALENCIA
# ============================================================================
def verificar(semilla=12345, n_pasos=5000):
    """Comprueba que lotes encadenados == corrida continua.

    Parámetros
    ----------
    semilla : int, opcional (default=12345)
    n_pasos : int, opcional (default=5000)

    Retorna
    -------
    bool
        True si ambas corridas dan la misma posición final.
    """
    a, _, _ = simular_replica(semilla, n_pasos, n_lote=n_pasos)
    b, _, _ = simular_replica(semilla, n_pasos, n_lote=137)
    ok = (a == b)
    print(f"Continuo: {a} | Lotes de 137: {b} -> "
          f"{'OK, equivalentes' if ok else 'ERROR'}")
    return ok


# ============================================================================
# 6. ANÁLISIS Y VISUALIZACIONES
# ============================================================================
def resumir(finales, n_pasos):
    """Imprime estadísticas descriptivas y valida contra teoría.

    Parámetros
    ----------
    finales : np.ndarray[int]
    n_pasos : int
    """
    sigma = math.sqrt(n_pasos)
    print("=" * 60)
    print(f"Réplicas: {len(finales)} | pasos: {n_pasos}")
    print(f"Media: {finales.mean():.2f} (teórica 0)")
    print(f"Desv. est.: {finales.std(ddof=1):.2f} (teórica {sigma:.2f})")
    print(f"Mín/Máx: {finales.min()} / {finales.max()}")
    print(f"Dentro de ±1σ: {np.mean(np.abs(finales) <= sigma):.1%} (normal: 68.3%)")
    print(f"Dentro de ±2σ: {np.mean(np.abs(finales) <= 2*sigma):.1%} (normal: 95.4%)")
    print(f"Paridad correcta: {bool(np.all(finales % 2 == n_pasos % 2))}")
    print("=" * 60)


def graficar_histograma(finales, n_pasos, ruta):
    """Histograma de posiciones finales + curva normal teórica.

    Parámetros
    ----------
    finales : np.ndarray[int]
    n_pasos : int
    ruta : str
    """
    sigma = math.sqrt(n_pasos)
    plt.figure(figsize=(8, 5))
    plt.hist(finales, bins=20, density=True, edgecolor="black",
             alpha=0.7, label="Simulación")
    x = np.linspace(-4*sigma, 4*sigma, 400)
    plt.plot(x, np.exp(-x**2 / (2*sigma**2)) / (sigma*math.sqrt(2*math.pi)),
             "r-", lw=2, label=f"Normal(0, {sigma:.0f}²)")
    plt.xlabel("Posición final")
    plt.ylabel("Densidad")
    plt.title(f"Posiciones finales tras {n_pasos:,} pasos ({len(finales)} réplicas)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"Guardado: {ruta}")


def graficar_trayectorias(semillas, n_pasos, n_lote, ruta, n_mostrar=10):
    """Dibuja unas pocas trayectorias para visualizar la caminata.

    Parámetros
    ----------
    semillas : list[int]
    n_pasos : int
    n_lote : int
    ruta : str
    n_mostrar : int, opcional (default=10)
    """
    plt.figure(figsize=(10, 5))
    for s in semillas[:n_mostrar]:
        _, _, tray = simular_replica(s, n_pasos, n_lote, guardar_tray=True)
        x = np.arange(1, len(tray) + 1) * n_lote
        plt.plot(x, tray, lw=0.8, alpha=0.7)
    plt.axhline(0, color="black", lw=0.5, ls="--")
    plt.xlabel("Paso")
    plt.ylabel("Posición")
    plt.title(f"Trayectorias de {n_mostrar} réplicas (1D)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"Guardado: {ruta}")


# ============================================================================
# 7. MAIN
# ============================================================================
def main(argv=None):
    """Punto de entrada.

    Parámetros
    ----------
    argv : list[str] | None
        Argumentos CLI.
    """
    p = argparse.ArgumentParser(description="Caminata aleatoria 1D por lotes.")
    p.add_argument("--semilla", type=int, default=12345)
    p.add_argument("--n_rep", type=int, default=100)
    p.add_argument("--n_pasos", type=int, default=1_000_000)
    p.add_argument("--n_lote", type=int, default=1000)
    p.add_argument("--archivo_semillas", default=None)
    p.add_argument("--salida", default="outputs")
    p.add_argument("--solo_verificar", action="store_true")
    p.add_argument("--trayectorias", action="store_true")

    if argv is None:
        args, _ = p.parse_known_args()
    else:
        args = p.parse_args(argv)

    if args.solo_verificar:
        return 0 if verificar() else 1

    semillas = (semillas_desde_archivo(args.archivo_semillas, args.n_rep)
                if args.archivo_semillas
                else semillas_desde_base(args.semilla, args.n_rep))
    os.makedirs(args.salida, exist_ok=True)

    print("Iniciando simulación principal...")
    t0 = time.perf_counter()
    finales, pos_m, vis_m = simular(semillas, args.n_pasos, args.n_lote)
    t = time.perf_counter() - t0

    resumir(finales, args.n_pasos)
    if len(pos_m):
        print(f"Retorno exacto en paso 1000: {np.mean(pos_m == 0):.4f} (teórico 0.0252)")
        print(f"Paso por el origen en ≤1000: {vis_m.mean():.4f} (teórico 0.9748)")
    print(f"Tiempo: {t:.2f} s")

    graficar_histograma(finales, args.n_pasos,
                        os.path.join(args.salida, "histograma_1d.png"))
    if args.trayectorias:
        graficar_trayectorias(semillas, min(args.n_pasos, 100_000), args.n_lote,
                              os.path.join(args.salida, "trayectorias_1d.png"))

    with open(os.path.join(args.salida, "finales_1d.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["replica", "semilla", "posicion_final"])
        for i, (s, x) in enumerate(zip(semillas, finales)):
            w.writerow([i, s, x])

    print(f"\nTodo guardado en '{args.salida}/'")


if __name__ == "__main__":
    main()