import json
import os
import pickle
import time

from src import configuracion, estudio, graficas
from src.generadores import generador_temporal

SEMILLA_BASE = 12345
CARPETA_SALIDA = "outputs"


def guardar_figura(figura, nombre):
    ruta = os.path.join(CARPETA_SALIDA, nombre)
    figura.savefig(ruta, dpi=150, bbox_inches="tight")


def main():
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    parametros = configuracion.parametros_por_defecto()
    n_simulaciones = parametros["n_simulaciones"]

    inicio = time.time()

    resultados_sin_vacunacion = estudio.correr_estudio(
        parametros, generador_temporal, SEMILLA_BASE, n_simulaciones, forzar_sin_vacunacion=True
    )
    resultados_con_vacunacion = estudio.correr_estudio(
        parametros, generador_temporal, SEMILLA_BASE + 10_000_000, n_simulaciones, forzar_sin_vacunacion=False
    )

    duracion_segundos = time.time() - inicio

    with open(os.path.join(CARPETA_SALIDA, "resultados_sin_vacunacion.pkl"), "wb") as archivo:
        pickle.dump(resultados_sin_vacunacion, archivo)
    with open(os.path.join(CARPETA_SALIDA, "resultados_con_vacunacion.pkl"), "wb") as archivo:
        pickle.dump(resultados_con_vacunacion, archivo)

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

    resumen = {
        "semilla_base": SEMILLA_BASE,
        "n_simulaciones_por_escenario": n_simulaciones,
        "duracion_segundos": duracion_segundos,
        "estadisticas_sin_vacunacion": fila_sin,
        "estadisticas_con_vacunacion": fila_con,
        "sensibilidad_total_infectados": filas_sensibilidad_infectados,
        "sensibilidad_total_muertes": filas_sensibilidad_muertes,
    }

    with open(os.path.join(CARPETA_SALIDA, "resumen_estudio.json"), "w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, indent=2, ensure_ascii=False)

    print(f"Estudio completo terminado en {duracion_segundos:.1f} segundos")
    print(f"Resultados guardados en {CARPETA_SALIDA}/")


if __name__ == "__main__":
    main()
