"""Simulación 2D de la rana por lotes encadenados.

Descripción general
-------------------
Se simula una caminata aleatoria simétrica en el plano. La rana parte del
origen (0, 0) y en cada paso se mueve en una de cuatro direcciones
(arriba, abajo, izquierda, derecha), cada una con probabilidad 0.25.
Tras `n_pasos` se registra la posición final y se repite el experimento
`n_rep` veces con semillas distintas.


Estrategia de simulación
------------------------
La caminata se simula por LOTES encadenados. El estado que pasa de un
lote al siguiente es:
    1. Posición final del lote anterior  -> posición inicial del siguiente.
    2. Estado interno del generador      -> continúa la secuencia pseudoaleatoria.
    3. Flag "ya volvió al origen después del paso 1000" -> se arrastra.

Arquitectura
------------
- Los generadores producen enteros Xi.
- El módulo de distribuciones los convierte a uniformes Ri en [0, 1).
- La caminata usa los Ri para decidir la dirección de cada paso.
- Las pruebas de validación validan los uniformes generados.

Convenciones y notación
-----------------------
Variables de la caminata:
- `pos`   : posición actual (x, y). Tupla de enteros. Se arrastra entre lotes.
- `paso`  : cada movimiento individual, uno de (1,0), (-1,0), (0,1), (0,-1).
- `tray`  : trayectoria acumulada dentro de un lote (arrays de x e y).
- `visito_despues` : bool. True si la rana volvió al origen después del paso 1000.
- `marca` : paso específico (default 1000) usado como referencia.

Cantidades:
- `n_pasos` : pasos totales por réplica (default 1_000_000).
- `n_rep`   : número de réplicas (default 100).
- `n_lote`  : tamaño de cada lote (default 1000).
- `hecho`   : pasos ya completados (contador interno).
- `tam`     : tamaño del lote actual. Vale min(n_lote, n_pasos - hecho).
- `m`       : módulo del generador.

Variables aleatorias:
- `Xi` : entero producido por el generador, en [0, m).
- `Ri` : uniforme en [0, 1) = Xi / m. Se usa para decidir la dirección.
"""

import argparse
import csv
import math
import os
import sys
import time
import resource

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np



# Rutas a los módulos del Punto 3
RUTA_PUNTO_3 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "punto 3 - generadores", "src"
)
sys.path.insert(0, RUTA_PUNTO_3)

# Generadores
from generadores.congruencial import (
    congruencial_lineal,
    congruencial_multiplicativo,
)
from generadores.cuadrados_medios import cuadrados_medios

# Distribuciones
from generadores.distribuciones import uniforme_desde_enteros

# Pruebas de validación
from validacion.prueba_chi_cuadrado import chi_square_test
from validacion.prueba_kolmogorov_smirnov import ks_test
from validacion.prueba_medias import means_test
from validacion.prueba_poker import poker_test
from validacion.prueba_rachas import runs_test
from validacion.prueba_varianza import variance_test


# 1. WRAPPER DE GENERADORES
class GeneradorConectado:
    """Envuelve un generador para que la caminata lo use.

    Parámetros del constructor
    --------------------------
    funcion : callable
        Función generadora. Debe aceptar `**kwargs`.
    modulo : int
        Módulo del generador. Se usa para normalizar Xi -> Ri.
    nombre_cantidad : str, opcional (default="cantidad")
        Nombre del parámetro que indica cuántos valores generar.
    nombre_semilla : str, opcional (default="semilla")
        Nombre del parámetro que guarda el estado (semilla).
    **parametros : dict
        Parámetros fijos del generador (a, c, m, n_digitos, etc.).
        Deben incluir la semilla inicial con el nombre `nombre_semilla`.
    """

    def __init__(self, funcion, modulo, nombre_cantidad="cantidad",
                 nombre_semilla="semilla", **parametros):
        if nombre_semilla not in parametros:
            raise ValueError(f"Se requiere '{nombre_semilla}' en los parámetros.")
        self.funcion = funcion
        self.m = modulo
        self.nombre_cantidad = nombre_cantidad
        self.nombre_semilla = nombre_semilla
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
        kwargs = {self.nombre_cantidad: cantidad, **self.parametros}
        enteros = self.funcion(**kwargs)
        self.parametros[self.nombre_semilla] = enteros[-1]
        return uniforme_desde_enteros(enteros, self.m)


# 2. CONFIGURACIÓN DE GENERADORES
def crear_generador(semilla, tipo="multiplicativo"):
    """Crea un generador conectado a la caminata.

    Parámetros
    ----------
    semilla : int
    tipo : str, opcional (default="multiplicativo")
        "cuadrados_medios", "lineal" o "multiplicativo".

    Retorna
    -------
    GeneradorConectado
    """
    if tipo == "cuadrados_medios":
        n_digitos = 4
        m = 10 ** n_digitos
        return GeneradorConectado(
            funcion=cuadrados_medios,
            modulo=m,
            nombre_cantidad="cantidad",
            nombre_semilla="semilla",
            semilla=semilla % m,
            n_digitos=n_digitos,
        )
    elif tipo == "lineal":
        m = 2 ** 31
        a = 1103515245
        c = 12345
        s = semilla % m
        return GeneradorConectado(
            funcion=congruencial_lineal,
            modulo=m,
            nombre_cantidad="count",
            nombre_semilla="seed",
            seed=s,
            a=a,
            c=c,
            m=m,
        )
    elif tipo == "multiplicativo":
        m = 2 ** 31
        a = 1103515245
        s = semilla % m
        if s == 0:
            s = 1
        return GeneradorConectado(
            funcion=congruencial_multiplicativo,
            modulo=m,
            nombre_cantidad="count",
            nombre_semilla="seed",
            seed=s,
            a=a,
            m=m,
        )
    else:
        raise ValueError(
            f"Generador '{tipo}' no reconocido. "
            "Use 'cuadrados_medios', 'lineal' o 'multiplicativo'."
        )


# 3. SEMILLAS
def semillas_desde_base(semilla_base, n_rep):
    """Genera `n_rep` semillas separadas por la constante de Weyl."""
    return [(semilla_base + i * 2654435761) % 2**32 for i in range(n_rep)]


def semillas_desde_archivo(ruta, n_rep):
    """Lee semillas desde un archivo .txt o .csv."""
    with open(ruta, encoding="utf-8") as f:
        texto = f.read().replace(",", " ").replace(";", " ")
    semillas = [int(t) for t in texto.split()]
    if len(semillas) < n_rep:
        raise ValueError(f"El archivo tiene {len(semillas)} semillas y se piden {n_rep}.")
    return semillas[:n_rep]



# 4. DIRECCIONES EN 2D
    # 4 direcciones: derecha (+x), izquierda (-x), arriba (+y), abajo (-y).
    # Cada una con probabilidad 0.25. Se decide con 1 uniforme por paso.
DIRECCIONES_2D = np.array([
    (1, 0),    # derecha
    (-1, 0),   # izquierda
    (0, 1),    # arriba
    (0, -1),   # abajo
], dtype=np.int64)


def uniformes_a_pasos_2d(u):
    """Convierte un array de uniformes en [0,1) a pasos 2D.

    Cada u se mapea a una de las 4 direcciones según en qué cae:
        u < 0.25   -> (1, 0)   derecha
        0.25-0.50  -> (-1, 0)  izquierda
        0.50-0.75  -> (0, 1)   arriba
        0.75-1.00  -> (0, -1)  abajo

    Parámetros
    ----------
    u : np.ndarray
        Uniformes en [0, 1).

    Retorna
    -------
    pasos : np.ndarray, shape (n, 2)
        Un vector unitario por cada u.
    """
    idx = np.minimum((u * 4).astype(np.int64), 3)
    return DIRECCIONES_2D[idx]


# 5. SIMULACIÓN POR LOTES
def avanzar_lote(gen, pos_x, pos_y, visito_despues, n_lote, paso_inicio,
                 marca=1000):
    """Avanza `n_lote` pasos partiendo del estado recibido.

    Parámetros
    ----------
    gen : GeneradorConectado
    pos_x, pos_y : int
        Posición actual (x, y).
    visito_despues : bool
        True si ya volvió al origen después del paso `marca`.
    n_lote : int
    paso_inicio : int
    marca : int, opcional (default=1000)

    Retorna
    -------
    nuevo_x, nuevo_y : int
    nuevo_visito_despues : bool
    """
    u = np.asarray(gen.siguiente_lote(n_lote))
    pasos = uniformes_a_pasos_2d(u)

    # Trayectoria acumulada de x e y dentro del lote.
    tray_x = pos_x + np.cumsum(pasos[:, 0], dtype=np.int64)
    tray_y = pos_y + np.cumsum(pasos[:, 1], dtype=np.int64)

    # Actualizar flag de retorno al origen después del paso 1000.
    nuevo_visito_despues = visito_despues
    if not nuevo_visito_despues:
        # Índice del primer paso del lote que cae después del paso 1000.
        desde = max(0, (marca + 1) - paso_inicio)
        if desde < len(tray_x):
            # ¿Hay algún (0, 0) en la parte del lote después del 1000?
            mascara = (tray_x[desde:] == 0) & (tray_y[desde:] == 0)
            if mascara.any():
                nuevo_visito_despues = True

    return int(tray_x[-1]), int(tray_y[-1]), nuevo_visito_despues


def simular_replica(semilla, n_pasos, n_lote, marca=1000, guardar_tray=False,
                    tipo="multiplicativo"):
    """Simula UNA réplica completa.

    Retorna
    -------
    pos_x, pos_y : int
        Posición final.
    visito_despues : bool
        True si volvió al origen después del paso `marca`.
    tray_x, tray_y : list[int] | None
        Trayectoria muestreada al final de cada lote (si guardar_tray).
    """
    gen = crear_generador(semilla, tipo=tipo)
    pos_x, pos_y, visito_despues, hecho = 0, 0, False, 0
    tray_x = [] if guardar_tray else None
    tray_y = [] if guardar_tray else None

    while hecho < n_pasos:
        tam = min(n_lote, n_pasos - hecho)
        pos_x, pos_y, visito_despues = avanzar_lote(
            gen, pos_x, pos_y, visito_despues, tam, hecho, marca
        )
        hecho += tam
        if guardar_tray:
            tray_x.append(pos_x)
            tray_y.append(pos_y)

    return pos_x, pos_y, visito_despues, (tray_x, tray_y)


def simular(semillas, n_pasos, n_lote, marca=1000, tipo="multiplicativo"):
    """Simula todas las réplicas.

    Retorna
    -------
    finales_x : np.ndarray[int]
    finales_y : np.ndarray[int]
    visito_despues : np.ndarray[bool]
    """
    finales_x, finales_y, visito_despues = [], [], []
    for s in semillas:
        px, py, vd, _ = simular_replica(s, n_pasos, n_lote, marca, tipo=tipo)
        finales_x.append(px)
        finales_y.append(py)
        visito_despues.append(vd)
    return np.array(finales_x), np.array(finales_y), np.array(visito_despues)


# 6. VERIFICACIÓN
def verificar(semilla=12345, n_pasos=5000, tipo="multiplicativo"):
    """Comprueba que lotes encadenados == corrida continua.

    Parámetros
    ----------
    semilla : int, opcional (default=12345)
    n_pasos : int, opcional (default=5000)
    tipo : str, opcional (default="multiplicativo")

    Retorna
    -------
    bool
    """
    a = simular_replica(semilla, n_pasos, n_lote=n_pasos, tipo=tipo)[:2]
    b = simular_replica(semilla, n_pasos, n_lote=137, tipo=tipo)[:2]
    ok = (a == b)
    print(f"Continuo: {a} | Lotes de 137: {b} -> "
          f"{'OK, equivalentes' if ok else 'ERROR'}")
    return ok


# 7. VALIDACIÓN DEL CONJUNTO
def _extraer_pasa(resultado):
    """Extrae el booleano de pasa/no pasa de un dict de prueba."""
    for clave in ("passed_test", "passes_test", "pasa_prueba", "pasa"):
        if clave in resultado:
            return bool(resultado[clave])
    return None


def validar_conjunto(semilla=12345, cantidad=10000, tipo="multiplicativo"):
    """Valida el conjunto generador + distribuciones.

    Corre las 6 pruebas del Punto 3 sobre los uniformes del generador.

    Parámetros
    ----------
    semilla : int, opcional (default=12345)
    cantidad : int, opcional (default=10000)
    tipo : str, opcional (default="multiplicativo")

    Retorna
    -------
    bool
    """
    print("=" * 65)
    print(f"VALIDACIÓN DEL CONJUNTO (generador: {tipo})")
    print("=" * 65)

    gen = crear_generador(semilla, tipo=tipo)
    u = gen.siguiente_lote(cantidad)
    u_lista = [float(x) if 0 < x < 1 else 0.5 for x in u]

    resultados = {}

    r = means_test(u_lista)
    pasa = _extraer_pasa(r)
    resultados["medias"] = pasa
    media = r.get("mean", r.get("promedio", 0))
    print(f"1. Medias:     media={float(media):.4f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    r = variance_test(u_lista)
    pasa = _extraer_pasa(r)
    resultados["varianza"] = pasa
    var = r.get("variance", r.get("varianza", 0))
    print(f"2. Varianza:   var={float(var):.5f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    r = chi_square_test(u_lista, n_intervals=10)
    pasa = _extraer_pasa(r)
    resultados["chi2"] = pasa
    print(f"3. Chi²:       stat={r.get('statistic', 0):.4f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    r = ks_test(u_lista)
    pasa = _extraer_pasa(r)
    resultados["ks"] = pasa
    print(f"4. KS:         D={r.get('d_max', 0):.4f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    r = poker_test(u_lista)
    pasa = _extraer_pasa(r)
    resultados["poker"] = pasa
    print(f"5. Póker:      stat={r.get('statistic', 0):.4f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    r = runs_test(u_lista)
    pasa = _extraer_pasa(r)
    resultados["rachas"] = pasa
    print(f"6. Rachas:     runs={r.get('num_runs', 0)}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    print("=" * 65)
    todo_ok = all(resultados.values())
    print(f"RESULTADO: {'TODO OK' if todo_ok else 'HAY FALLOS'}")
    print("=" * 65)
    return todo_ok


# 8. ANÁLISIS Y VISUALIZACIONES
def resumir(finales_x, finales_y, n_pasos, visito_despues):
    """Imprime estadísticas descriptivas.

    Parámetros
    ----------
    finales_x, finales_y : np.ndarray[int]
    n_pasos : int
    visito_despues : np.ndarray[bool]
    """
    sigma = math.sqrt(n_pasos)
    n = len(finales_x)
    print("=" * 60)
    print(f"Réplicas: {n} | pasos: {n_pasos} | dimensión: 2D")
    print(f"Media x: {finales_x.mean():.2f} (teórica 0)")
    print(f"Media y: {finales_y.mean():.2f} (teórica 0)")
    print(f"Desv. x: {finales_x.std(ddof=1):.2f} (teórica {sigma:.2f})")
    print(f"Desv. y: {finales_y.std(ddof=1):.2f} (teórica {sigma:.2f})")
    print(f"Mín/Máx x: {finales_x.min()} / {finales_x.max()}")
    print(f"Mín/Máx y: {finales_y.min()} / {finales_y.max()}")
    print(f"Retorno al origen DESPUÉS del paso 1000: {visito_despues.mean():.4f}")
    print("=" * 60)


def graficar_scatter(finales_x, finales_y, n_pasos, ruta):
    """Scatter plot de las posiciones finales en 2D.

    Parámetros
    ----------
    finales_x, finales_y : np.ndarray[int]
    n_pasos : int
    ruta : str
    """
    sigma = math.sqrt(n_pasos)
    plt.figure(figsize=(7, 7))
    plt.scatter(finales_x, finales_y, s=30, alpha=0.7, edgecolors="black")
    plt.axhline(0, color="gray", lw=0.5, ls="--")
    plt.axvline(0, color="gray", lw=0.5, ls="--")
    plt.scatter([0], [0], s=80, color="red", marker="x",
                linewidths=2, label="Origen")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Posiciones finales 2D tras {n_pasos:,} pasos ({len(finales_x)} réplicas)")
    plt.axis("equal")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"Guardado: {ruta}")


def graficar_trayectorias(semillas, n_pasos, n_lote, ruta, n_mostrar=10,
                          tipo="multiplicativo"):
    """Dibuja unas pocas trayectorias 2D.

    Parámetros
    ----------
    semillas : list[int]
    n_pasos : int
    n_lote : int
    ruta : str
    n_mostrar : int, opcional (default=10)
    tipo : str, opcional (default="multiplicativo")
    """
    plt.figure(figsize=(8, 8))
    for s in semillas[:n_mostrar]:
        _, _, _, (tx, ty) = simular_replica(
            s, n_pasos, n_lote, guardar_tray=True, tipo=tipo
        )
        plt.plot(tx, ty, lw=0.8, alpha=0.7)
    plt.scatter([0], [0], s=80, color="red", marker="x",
                linewidths=2, label="Origen")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Trayectorias 2D de {n_mostrar} réplicas")
    plt.axis("equal")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"Guardado: {ruta}")


# 9. MAIN
def main(argv=None):
    """Punto de entrada."""
    p = argparse.ArgumentParser(description="Caminata aleatoria 2D por lotes.")
    p.add_argument("--semilla", type=int, default=12345)
    p.add_argument("--n_rep", type=int, default=100)
    p.add_argument("--n_pasos", type=int, default=1_000_000)
    p.add_argument("--n_lote", type=int, default=1000)
    p.add_argument("--generador", default="multiplicativo",
                   choices=["cuadrados_medios", "lineal", "multiplicativo"],
                   help="Tipo de generador a usar.")
    p.add_argument("--archivo_semillas", default=None)
    p.add_argument("--salida", default="outputs/2d")
    p.add_argument("--solo_verificar", action="store_true")
    p.add_argument("--validar", action="store_true")
    p.add_argument("--trayectorias", action="store_true")

    if argv is None:
        args, _ = p.parse_known_args()
    else:
        args = p.parse_args(argv)

    if args.validar:
        return 0 if validar_conjunto(tipo=args.generador) else 1

    if args.solo_verificar:
        return 0 if verificar(tipo=args.generador) else 1

    semillas = (semillas_desde_archivo(args.archivo_semillas, args.n_rep)
                if args.archivo_semillas
                else semillas_desde_base(args.semilla, args.n_rep))
    os.makedirs(args.salida, exist_ok=True)

    print(f"Iniciando simulación 2D (generador: {args.generador})...")
    t0 = time.perf_counter()
    finales_x, finales_y, vis_despues = simular(
        semillas, args.n_pasos, args.n_lote, tipo=args.generador
    )
    t = time.perf_counter() - t0

    resumir(finales_x, finales_y, args.n_pasos, vis_despues)
    mem_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"Tiempo: {t:.2f} s | Memoria pico: {mem_mb:.0f} MB")

    graficar_scatter(finales_x, finales_y, args.n_pasos,
                     os.path.join(args.salida, "scatter_2d.png"))
    if args.trayectorias:
        graficar_trayectorias(semillas, min(args.n_pasos, 100_000), args.n_lote,
                              os.path.join(args.salida, "trayectorias_2d.png"),
                              tipo=args.generador)

    with open(os.path.join(args.salida, "finales_2d.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["replica", "semilla", "x_final", "y_final", "visito_despues"])
        for i, (s, x, y, vd) in enumerate(zip(semillas, finales_x, finales_y, vis_despues)):
            w.writerow([i, s, x, y, bool(vd)])

    print(f"\nTodo guardado en '{args.salida}/'")


if __name__ == "__main__":
    main()