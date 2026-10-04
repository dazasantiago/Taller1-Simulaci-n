import json
import os
import pickle
import sys
import time

from src import configuracion, estudio, graficas

SEMILLA_BASE = 12345
CARPETA_SALIDA = "outputs"


def guardar_figura(figura, nombre):
    ruta = os.path.join(CARPETA_SALIDA, nombre)
    figura.savefig(ruta, dpi=150, bbox_inches="tight")


def ruta_pickle(nombre):
    return os.path.join(CARPETA_SALIDA, f"resultados_{nombre}.pkl")


def correr_escenario(nombre, forzar_sin_vacunacion, semilla_base):
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    ruta = ruta_pickle(nombre)
    if os.path.exists(ruta):
        print(f"{nombre}: ya existe {ruta}, no se vuelve a correr")
        return

    parametros = configuracion.parametros_por_defecto()
    n_simulaciones = parametros["n_simulaciones"]

    inicio = time.time()
    resultados = estudio.correr_estudio(parametros, semilla_base, n_simulaciones, forzar_sin_vacunacion)
    duracion = time.time() - inicio

    with open(ruta, "wb") as archivo:
        pickle.dump(resultados, archivo)

    with open(os.path.join(CARPETA_SALIDA, f"duracion_{nombre}.json"), "w", encoding="utf-8") as archivo:
        json.dump({"duracion_segundos": duracion}, archivo)

    print(f"{nombre}: {n_simulaciones} simulaciones en {duracion:.1f} segundos, guardado en {ruta}")


def finalizar():
    with open(ruta_pickle("sin_vacunacion"), "rb") as archivo:
        resultados_sin_vacunacion = pickle.load(archivo)
    with open(ruta_pickle("con_vacunacion"), "rb") as archivo:
        resultados_con_vacunacion = pickle.load(archivo)

    parametros = configuracion.parametros_por_defecto()
    dias = list(range(parametros["dias_simulacion"]))

    curvas = {}
    campos_por_estado = (("S", "historial_s"), ("E", "historial_e"), ("I", "historial_i"), ("R", "historial_r"))
    for nombre_estado, campo in campos_por_estado:
        curvas[nombre_estado] = estudio.calcular_curva_promedio(resultados_con_vacunacion, campo)
    guardar_figura(graficas.graficar_curva_epidemica(dias, curvas), "01_curva_epidemica.png")

    totales_infectados = []
    for resultado in resultados_con_vacunacion:
        totales_infectados.append(resultado["total_infectados"])
    guardar_figura(
        graficas.graficar_histograma(totales_infectados, "Total de infectados", "Total de infectados"),
        "02_hist_total_infectados.png",
    )

    dias_pico = []
    for resultado in resultados_con_vacunacion:
        dias_pico.append(resultado["dia_pico"])
    guardar_figura(
        graficas.graficar_histograma(dias_pico, "Día del pico de infectados", "Día del pico"),
        "03_hist_dia_pico.png",
    )

    magnitudes_pico = []
    for resultado in resultados_con_vacunacion:
        magnitudes_pico.append(resultado["magnitud_pico"])
    guardar_figura(
        graficas.graficar_histograma(magnitudes_pico, "Magnitud del pico de infectados", "Infectados en el pico"),
        "04_hist_magnitud_pico.png",
    )

    dias_control = estudio.dias_hasta_control_validos(resultados_con_vacunacion)
    if len(dias_control) > 0:
        guardar_figura(
            graficas.graficar_histograma(dias_control, "Días hasta el control del brote", "Día de control"),
            "05_hist_dias_control.png",
        )

    totales_muertes = []
    for resultado in resultados_con_vacunacion:
        totales_muertes.append(resultado["total_muertes"])
    guardar_figura(
        graficas.graficar_histograma(totales_muertes, "Total de muertes", "Total de muertes"),
        "06_hist_total_muertes.png",
    )

    promedio_i_sin, _, _ = estudio.calcular_curva_promedio(resultados_sin_vacunacion, "historial_i")
    promedio_i_con, _, _ = estudio.calcular_curva_promedio(resultados_con_vacunacion, "historial_i")
    guardar_figura(
        graficas.graficar_comparacion_escenarios(dias, promedio_i_sin, promedio_i_con),
        "07_comparacion_escenarios.png",
    )

    filas_sensibilidad_infectados = estudio.analizar_sensibilidad(resultados_con_vacunacion, "total_infectados")
    guardar_figura(graficas.graficar_tornado(filas_sensibilidad_infectados), "08_tornado_infectados.png")

    filas_sensibilidad_muertes = estudio.analizar_sensibilidad(resultados_con_vacunacion, "total_muertes")
    guardar_figura(graficas.graficar_tornado(filas_sensibilidad_muertes), "09_tornado_muertes.png")

    fila_sin = estudio.calcular_estadisticas_escenario(resultados_sin_vacunacion)
    fila_con = estudio.calcular_estadisticas_escenario(resultados_con_vacunacion)
    fila_sin["escenario"] = "Sin vacunación"
    fila_con["escenario"] = "Con vacunación"

    duracion_total = 0
    for nombre in ("sin_vacunacion", "con_vacunacion"):
        with open(os.path.join(CARPETA_SALIDA, f"duracion_{nombre}.json"), encoding="utf-8") as archivo:
            duracion_total += json.load(archivo)["duracion_segundos"]

    resumen = {
        "semilla_base": SEMILLA_BASE,
        "n_simulaciones_por_escenario": parametros["n_simulaciones"],
        "duracion_segundos": duracion_total,
        "estadisticas_sin_vacunacion": fila_sin,
        "estadisticas_con_vacunacion": fila_con,
        "sensibilidad_total_infectados": filas_sensibilidad_infectados,
        "sensibilidad_total_muertes": filas_sensibilidad_muertes,
    }

    with open(os.path.join(CARPETA_SALIDA, "resumen_estudio.json"), "w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, indent=2, ensure_ascii=False)

    print(f"Resultados finales guardados en {CARPETA_SALIDA}/")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "todo"

    if modo == "sin_vacunacion":
        correr_escenario("sin_vacunacion", True, SEMILLA_BASE)
    elif modo == "con_vacunacion":
        correr_escenario("con_vacunacion", False, SEMILLA_BASE + 10_000_000)
    elif modo == "finalizar":
        finalizar()
    else:
        correr_escenario("sin_vacunacion", True, SEMILLA_BASE)
        correr_escenario("con_vacunacion", False, SEMILLA_BASE + 10_000_000)
        finalizar()
