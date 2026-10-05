"""Simulación 1D de la rana por lotes encadenados.

Descripción general
-------------------
Se simula una caminata aleatoria simétrica en una recta numérica infinita:
la rana parte del origen (posición 0) y en cada paso se mueve +1 o -1 con
idéntica probabilidad (0.5 cada uno). Tras `n_pasos` se registra la posición
final, y se repite el experimento `n_rep` veces con semillas distintas.

Estrategia de simulación
---------------------------------------------------
La caminata se simula por LOTES encadenados. El estado que pasa de un lote
al siguiente es:
    1. Posición final del lote anterior  -> posición inicial del siguiente.
    2. Estado interno del generador      -> continúa la secuencia pseudoaleatoria del generador.
    3. Flag que marca si ya pasó por el origen      -> se arrastra entre lotes.

Encadenar los lotes y mantener el estado del generador entre iteraciones 
permite simular una sola repeticion de la caminata sin necesidad de generar todos los pasos de una vez.

Arquitectura
------------
- Los generadores producen enteros Xi.
- El módulo de distribuciones los convierte a uniformes Ri en [0, 1).
- La caminata usa los Ri para decidir cada paso (+1 si Ri < 0.5, -1 si no).
- Las pruebas de validación validan los uniformes generados.

El wrapper `GeneradorConectado`  permite unir el generador
y la caminata. Adaptandose a los nombres de los parámetros de cada generador.

Convenciones y notación
-----------------------
Variables de la caminata:
- `pos`       : posición actual de la rana. Entero. Se arrastra entre lotes.
- `paso`      : cada movimiento individual (+1 o -1).
- `tray`      : trayectoria acumulada dentro de un lote.
- `visito`    : bool. True si la rana ya tocó el origen (pos=0).
- visito_despues : bool. True si la rana volvió al origen después del paso 1000.
- `marca`     : paso específico (default 1000) donde se registra pos y visito.

Cantidades:
- `n_pasos`   : pasos totales por réplica (default 1_000_000).
- `n_rep`     : número de réplicas (default 100).
- `n_lote`    : tamaño de cada lote (default 1000).
- `hecho`     : pasos ya completados (contador interno).
- `tam`       : tamaño del lote actual. Vale min(n_lote, n_pasos - hecho).
- `m`         : módulo del generador (ej: 10**4 para cuadrados medios).

Variables aleatorias:
- `Xi`        : entero producido por el generador, en [0, m).
- `Ri`        : uniforme en [0, 1) = Xi / m. Se usa para decidir el paso.
- `sigma`     : desviación estándar teórica = sqrt(n_pasos).
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


# Rutas a los módulos de generadores
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
from validacion.prueba_chi_cuadrado import chi_square_test
from validacion.prueba_kolmogorov_smirnov import ks_test

# Pruebas de validación
from validacion.prueba_medias import means_test
from validacion.prueba_poker import poker_test
from validacion.prueba_rachas import runs_test
from validacion.prueba_varianza import variance_test

# 1. WRAPPER DE GENERADORES
class GeneradorConectado:
    """Envuelve un generador para que la caminata lo use.

    Parámetros del constructor
    --------------------------
    funcion : 
        Función generadora. Debe aceptar `**kwargs`.

    modulo : int
        Módulo del generador. Se usa para normalizar Xi -> Ri.

    nombre_cantidad : str, opcional (default="cantidad")
        Nombre del parámetro que indica cuántos valores generar.

    nombre_semilla : str, opcional (default="semilla")
        Nombre del parámetro que guarda el estado (semilla).

    **parametros : dict
        Parámetros fijos del generador (a, c, m, n_digitos, etc.).
        se debe incluir la semilla inicial con el nombre `nombre_semilla`.
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
        # Encadenamiento: el último entero es la nueva semilla.
        self.parametros[self.nombre_semilla] = enteros[-1]
        return uniforme_desde_enteros(enteros, self.m)


# 2. CONFIGURACIÓN DE GENERADORES
def crear_generador(semilla, tipo="multiplicativo"):
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
    """Genera `n_rep` semillas.

    Parámetros
    ----------
        semilla_base : int
        n_rep : int

    Retorna
    -------
        list[int]
    """
    return [(semilla_base + i * 2654435761) % 2**32 for i in range(n_rep)]


def semillas_desde_archivo(ruta, n_rep):
    """Lee semillas desde un archivo .txt o .csv.

    Parámetros
    ----------
        ruta : str
        n_rep : int

    Retorna
    -------
        list[int]
    """
    with open(ruta, encoding="utf-8") as f:
        texto = f.read().replace(",", " ").replace(";", " ")
    semillas = [int(t) for t in texto.split()]
    if len(semillas) < n_rep:
        raise ValueError(f"El archivo tiene {len(semillas)} semillas y se piden {n_rep}.")
    return semillas[:n_rep]



# 4. SIMULACIÓN POR LOTES
def avanzar_lote(gen, pos, visito, visito_despues, n_lote, paso_inicio, marca=1000):
    """Avanza `n_lote` pasos partiendo del estado recibido.

    Parámetros
    ----------
    gen : GeneradorConectado
    pos : int
    visito : bool
        True si ya tocó el origen hasta el paso `paso_inicio`.
    visito_despues : bool
        True si ya tocó el origen después del paso `marca`.
    n_lote : int
    paso_inicio : int
    marca : int, opcional (default=1000)

    Retorna
    -------
    nueva_pos : int
    nuevo_visito : bool
    nuevo_visito_despues : bool
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

    nuevo_visito = bool(visito or (tray == 0).any())

    nuevo_visito_despues = visito_despues
    if not nuevo_visito_despues:
        # Solo mirar la parte de la trayectoria que cae después del paso 1000.
        desde = max(0, (marca + 1) - paso_inicio)
        if desde < len(tray):
            if (tray[desde:] == 0).any():
                nuevo_visito_despues = True

    return int(tray[-1]), nuevo_visito, nuevo_visito_despues, registro


def simular_replica(semilla, n_pasos, n_lote, marca=1000, guardar_tray=False,
                    tipo="multiplicativo"):
    """Simula UNA réplica completa.

    Retorna
    -------
    pos : int
    reg : tuple(int, bool) | None
    visito_despues : bool
    trayectoria : list[int] | None
    """
    gen = crear_generador(semilla, tipo=tipo)
    pos, visito, visito_despues, hecho, reg = 0, False, False, 0, None
    trayectoria = [] if guardar_tray else None

    while hecho < n_pasos:
        tam = min(n_lote, n_pasos - hecho)
        pos, visito, visito_despues, r = avanzar_lote(
            gen, pos, visito, visito_despues, tam, hecho, marca
        )
        if r is not None:
            reg = r
        hecho += tam
        if guardar_tray:
            trayectoria.append(pos)

    return pos, reg, visito_despues, trayectoria


def simular(semillas, n_pasos, n_lote, marca=1000, tipo="multiplicativo"):
    """Simula todas las réplicas.

    Retorna
    -------
    finales : np.ndarray[int]
    pos_marca : np.ndarray[int]
    visito_marca : np.ndarray[bool]
    visito_despues : np.ndarray[bool]
    """
    finales, pos_marca, visito_marca, visito_despues = [], [], [], []
    for s in semillas:
        pos, reg, vd, _ = simular_replica(s, n_pasos, n_lote, marca, tipo=tipo)
        finales.append(pos)
        if reg is not None:
            pos_marca.append(reg[0])
            visito_marca.append(reg[1])
        visito_despues.append(vd)
    return (np.array(finales), np.array(pos_marca),
            np.array(visito_marca), np.array(visito_despues))


# 5. VERIFICACIÓN

def verificar(semilla=12345, n_pasos=5000, tipo="multiplicativo"):
    a, _, _, _ = simular_replica(semilla, n_pasos, n_lote=n_pasos, tipo=tipo)
    b, _, _, _ = simular_replica(semilla, n_pasos, n_lote=137, tipo=tipo)
    ok = (a == b)
    print(f"Continuo: {a} | Lotes de 137: {b} -> "
          f"{'OK, equivalentes' if ok else 'ERROR'}")
    return ok


# ============================================================================
# 6. VALIDACIÓN DEL CONJUNTO
# ============================================================================
def _extraer_pasa(resultado):
    """Extrae el booleano de pasa/no pasa de un dict de prueba."""
    for clave in ("passed_test", "passes_test", "pasa_prueba", "pasa"):
        if clave in resultado:
            return bool(resultado[clave])
    return None


def validar_conjunto(semilla=12345, cantidad=10000, tipo="multiplicativo"):
    """Valida el conjunto generador + distribuciones + caminata.

    Corre las 6 pruebas del Punto 3 sobre los uniformes del generador,
    y además valida la caminata.

    Parámetros
    ----------
        semilla : int, opcional (default=12345)
        cantidad : int, opcional (default=10000)
        tipo : str, opcional (default="multiplicativo")

    Retorna
    -------
    bool
        True si todas las validaciones pasan.
    """
    print("=" * 65)
    print(f"VALIDACIÓN DEL CONJUNTO (generador: {tipo})")
    print("=" * 65)

    gen = crear_generador(semilla, tipo=tipo)
    u = gen.siguiente_lote(cantidad)
    u_lista = [float(x) if 0 < x < 1 else 0.5 for x in u]

    resultados = {}

    # 1. Medias
    r = means_test(u_lista)
    pasa = _extraer_pasa(r)
    resultados["medias"] = pasa
    media = r.get("mean", r.get("promedio", 0))
    print(f"1. Medias:     media={float(media):.4f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    # 2. Varianza
    r = variance_test(u_lista)
    pasa = _extraer_pasa(r)
    resultados["varianza"] = pasa
    var = r.get("variance", r.get("varianza", 0))
    print(f"2. Varianza:   var={float(var):.5f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    # 3. Chi cuadrado
    r = chi_square_test(u_lista, n_intervals=10)
    pasa = _extraer_pasa(r)
    resultados["chi2"] = pasa
    print(f"3. Chi²:       stat={r.get('statistic', 0):.4f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    # 4. Kolmogorov-Smirnov
    r = ks_test(u_lista)
    pasa = _extraer_pasa(r)
    resultados["ks"] = pasa
    print(f"4. KS:         D={r.get('d_max', 0):.4f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    # 5. Póker
    r = poker_test(u_lista, hand_size=5)
    pasa = _extraer_pasa(r)
    resultados["poker"] = pasa
    print(f"5. Póker:      stat={r.get('statistic', 0):.4f}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    # 6. Rachas
    r = runs_test(u_lista)
    pasa = _extraer_pasa(r)
    resultados["rachas"] = pasa
    print(f"6. Rachas:     runs={r.get('num_runs', 0)}  "
          f"-> {'PASA' if pasa else 'FALLA'}")

    # Validación de la caminata
    print("-" * 65)
    print("Validación de la caminata (100 réplicas, 10000 pasos):")
    semillas = semillas_desde_base(semilla, 100)
    finales, _, _, _ = simular(semillas, 10000, 1000, tipo=tipo)
    sigma_teo = math.sqrt(10000)
    print(f"  Media: {finales.mean():.2f} (esperado 0)")
    print(f"  Desv:  {finales.std(ddof=1):.2f} (esperado {sigma_teo:.2f})")
    print(f"  Paridad: {bool((finales % 2 == 0).all())}")
    ok_caminata = bool((finales % 2 == 0).all())

    print("=" * 65)
    todo_ok = all(resultados.values()) and ok_caminata
    print(f"RESULTADO: {'TODO OK' if todo_ok else 'HAY FALLOS'}")
    print("=" * 65)
    return todo_ok


# ============================================================================
# 7. ANÁLISIS Y VISUALIZACIONES
# ============================================================================
def resumir(finales, n_pasos):
    """Imprime estadísticas descriptivas.

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
    print(f"Dentro de +-1 sigma: {np.mean(np.abs(finales) <= sigma):.1%} (normal: 68.3%)")
    print(f"Dentro de +-2 sigma: {np.mean(np.abs(finales) <= 2*sigma):.1%} (normal: 95.4%)")
    print(f"Paridad correcta: {bool(np.all(finales % 2 == n_pasos % 2))}")
    print("=" * 60)


def graficar_histograma(finales, n_pasos, ruta):
    """Histograma de posiciones finales + normal teórica.

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


def graficar_trayectorias(semillas, n_pasos, n_lote, ruta, n_mostrar=10,
                          tipo="multiplicativo"):
    """Dibuja unas pocas trayectorias para visualizar la caminata.

    Cada trayectoria es el camino completo de una réplica. Se grafican
    solo las primeras `n_mostrar` réplicas para que el gráfico sea
    legible (con 100 líneas encimadas no se distinguiría nada).

    Parámetros
    ----------
    semillas : list[int]
        Semillas de las réplicas. Se usan las primeras `n_mostrar`.
    n_pasos : int
        Pasos a mostrar. Conviene reducirlo (ej: 100_000) para que la
        dispersión se aprecie bien; con 1.000.000 las líneas quedan
        muy comprimidas.
    n_lote : int
        Tamaño de lote. La trayectoria se muestrea al final de cada lote.
    ruta : str
        Ruta donde guardar el PNG.
    n_mostrar : int, opcional (default=10)
        Cuántas réplicas dibujar.
    tipo : str, opcional (default="cuadrados_medios")
        Tipo de generador a usar para las réplicas.
    """
    plt.figure(figsize=(10, 5))
    for s in semillas[:n_mostrar]:
        _, _, _, tray = simular_replica(
            s, n_pasos, n_lote, guardar_tray=True, tipo=tipo
        )
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
# 8. MAIN
# ============================================================================
def main(argv=None):
    """Punto de entrada.

    Parámetros
    ----------
    argv : list[str] | None
        Argumentos CLI. Si es None, parsea sys.argv ignorando argumentos
        desconocidos.
    """
    p = argparse.ArgumentParser(description="Caminata aleatoria 1D por lotes.")
    p.add_argument("--semilla", type=int, default=12345)
    p.add_argument("--n_rep", type=int, default=100)
    p.add_argument("--n_pasos", type=int, default=1_000_000)
    p.add_argument("--n_lote", type=int, default=1000)
    p.add_argument("--generador", default="multiplicativo",
               choices=["cuadrados_medios", "lineal", "multiplicativo"],
               help="Tipo de generador a usar.")
    p.add_argument("--archivo_semillas", default=None)
    p.add_argument("--salida", default="outputs")
    p.add_argument("--solo_verificar", action="store_true")
    p.add_argument("--validar", action="store_true",
                   help="Corre la validación del conjunto y termina.")
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

    print(f"Iniciando simulación principal (generador: {args.generador})...")
    t0 = time.perf_counter()
    finales, pos_m, vis_m, vis_despues = simular(
        semillas, args.n_pasos, args.n_lote, tipo=args.generador
    )
    t = time.perf_counter() - t0

        resumir(finales, args.n_pasos)
    if len(pos_m):
        print(f"Retorno exacto en paso 1000: {np.mean(pos_m == 0):.4f} (teórico 0.0252)")
        print(f"Paso por el origen en ≤1000: {vis_m.mean():.4f} (teórico 0.9748)")
    print(f"Retorno al origen DESPUÉS del paso 1000: {vis_despues.mean():.4f} "
          f"(teórico ≈ 1.0000)")
    print(f"Tiempo: {t:.2f} s")
    graficar_histograma(finales, args.n_pasos,
                        os.path.join(args.salida, "histograma_1d.png"))
    if args.trayectorias:
        graficar_trayectorias(semillas, min(args.n_pasos, 100_000), args.n_lote,
                              os.path.join(args.salida, "trayectorias_1d.png"),
                              tipo=args.generador)

    with open(os.path.join(args.salida, "finales_1d.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["replica", "semilla", "posicion_final"])
        for i, (s, x) in enumerate(zip(semillas, finales)):
            w.writerow([i, s, x])

    print(f"\nTodo guardado en '{args.salida}/'")


if __name__ == "__main__":
    main()