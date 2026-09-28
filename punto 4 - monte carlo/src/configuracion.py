import csv
import io

N_POBLACION = 10000
INFECTADOS_INICIALES = 10
DIAS_SIMULACION = 365
N_SIMULACIONES = 1000

RANGO_BETA = (0.3, 0.5)
RANGO_SIGMA = (2, 5)
RANGO_GAMMA = (7, 14)
RANGO_P_TRANSMISION = (0.4, 0.6)
RANGO_TASA_VACUNACION = (0.3, 0.7)
RANGO_EFECTIVIDAD_VACUNA = (0.80, 0.95)


def parametros_por_defecto():
    return {
        "n_poblacion": N_POBLACION,
        "infectados_iniciales": INFECTADOS_INICIALES,
        "dias_simulacion": DIAS_SIMULACION,
        "n_simulaciones": N_SIMULACIONES,
        "rango_beta": RANGO_BETA,
        "rango_sigma": RANGO_SIGMA,
        "rango_gamma": RANGO_GAMMA,
        "rango_p_transmision": RANGO_P_TRANSMISION,
        "rango_tasa_vacunacion": RANGO_TASA_VACUNACION,
        "rango_efectividad_vacuna": RANGO_EFECTIVIDAD_VACUNA,
    }


def leer_configuracion_texto(texto):
    filas_por_nombre = {}
    lector = csv.DictReader(io.StringIO(texto))
    for fila in lector:
        filas_por_nombre[fila["parametro"]] = fila

    parametros = parametros_por_defecto()

    if "n_poblacion" in filas_por_nombre:
        parametros["n_poblacion"] = int(filas_por_nombre["n_poblacion"]["valor"])
    if "infectados_iniciales" in filas_por_nombre:
        parametros["infectados_iniciales"] = int(filas_por_nombre["infectados_iniciales"]["valor"])
    if "dias_simulacion" in filas_por_nombre:
        parametros["dias_simulacion"] = int(filas_por_nombre["dias_simulacion"]["valor"])
    if "n_simulaciones" in filas_por_nombre:
        parametros["n_simulaciones"] = int(filas_por_nombre["n_simulaciones"]["valor"])

    parametros["rango_beta"] = leer_rango(filas_por_nombre, "beta", parametros["rango_beta"])
    parametros["rango_sigma"] = leer_rango(filas_por_nombre, "sigma", parametros["rango_sigma"])
    parametros["rango_gamma"] = leer_rango(filas_por_nombre, "gamma", parametros["rango_gamma"])
    parametros["rango_p_transmision"] = leer_rango(filas_por_nombre, "p_transmision", parametros["rango_p_transmision"])
    parametros["rango_tasa_vacunacion"] = leer_rango(filas_por_nombre, "tasa_vacunacion", parametros["rango_tasa_vacunacion"])
    parametros["rango_efectividad_vacuna"] = leer_rango(filas_por_nombre, "efectividad_vacuna", parametros["rango_efectividad_vacuna"])

    return parametros


def leer_rango(filas_por_nombre, nombre, valor_por_defecto):
    if nombre not in filas_por_nombre:
        return valor_por_defecto
    fila = filas_por_nombre[nombre]
    minimo = float(fila["minimo"])
    maximo = float(fila["maximo"])
    return (minimo, maximo)


def cargar_configuracion(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        texto = archivo.read()
    return leer_configuracion_texto(texto)
