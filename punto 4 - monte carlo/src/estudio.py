from src import simulacion
from src.generador_adaptador import GeneradorMonteCarlo

NOMBRES_PARAMETROS_SENSIBILIDAD = (
    "beta",
    "p_transmision",
    "tasa_vacunacion",
    "dias_incubacion",
    "dias_infeccioso",
    "tasa_mortalidad",
)


def correr_estudio(configuracion, semilla_base, n_simulaciones, forzar_sin_vacunacion=False):
    resultados = []
    for i in range(n_simulaciones):
        generador = GeneradorMonteCarlo(semilla_base + i)
        resultado = simulacion.correr_una_simulacion(
            configuracion, generador.siguiente_uniforme, forzar_sin_vacunacion
        )
        resultados.append(resultado)
    return resultados


def promedio(lista):
    suma = 0
    for valor in lista:
        suma += valor
    return suma / len(lista)


def calcular_curva_promedio(resultados, campo):
    n_simulaciones = len(resultados)
    dias_simulacion = len(resultados[0][campo])

    curva_promedio = []
    curva_percentil_bajo = []
    curva_percentil_alto = []

    for dia in range(dias_simulacion):
        valores_dia = []
        for resultado in resultados:
            valores_dia.append(resultado[campo][dia])
        valores_dia.sort()

        curva_promedio.append(promedio(valores_dia))

        indice_bajo = int(0.025 * n_simulaciones)
        indice_alto = int(0.975 * n_simulaciones)
        if indice_alto >= n_simulaciones:
            indice_alto = n_simulaciones - 1

        curva_percentil_bajo.append(valores_dia[indice_bajo])
        curva_percentil_alto.append(valores_dia[indice_alto])

    return curva_promedio, curva_percentil_bajo, curva_percentil_alto


def calcular_estadisticas_escenario(resultados):
    totales_infectados = []
    totales_muertes = []
    dias_pico = []
    magnitudes_pico = []
    for resultado in resultados:
        totales_infectados.append(resultado["total_infectados"])
        totales_muertes.append(resultado["total_muertes"])
        dias_pico.append(resultado["dia_pico"])
        magnitudes_pico.append(resultado["magnitud_pico"])

    return {
        "total_infectados_promedio": promedio(totales_infectados),
        "total_infectados_minimo": min(totales_infectados),
        "total_infectados_maximo": max(totales_infectados),
        "total_muertes_promedio": promedio(totales_muertes),
        "total_muertes_minimo": min(totales_muertes),
        "total_muertes_maximo": max(totales_muertes),
        "dia_pico_promedio": promedio(dias_pico),
        "magnitud_pico_promedio": promedio(magnitudes_pico),
    }


def dias_hasta_control_validos(resultados):
    valores = []
    for resultado in resultados:
        if resultado["dias_hasta_control"] is not None:
            valores.append(resultado["dias_hasta_control"])
    return valores


def analizar_sensibilidad(resultados, campo_objetivo="total_infectados"):
    filas = []
    for nombre in NOMBRES_PARAMETROS_SENSIBILIDAD:
        valores_parametro = []
        for resultado in resultados:
            valores_parametro.append(resultado["parametros"][nombre])

        valores_ordenados = sorted(valores_parametro)
        mediana = valores_ordenados[len(valores_ordenados) // 2]

        grupo_bajo = []
        grupo_alto = []
        for resultado in resultados:
            if resultado["parametros"][nombre] <= mediana:
                grupo_bajo.append(resultado[campo_objetivo])
            else:
                grupo_alto.append(resultado[campo_objetivo])

        if len(grupo_bajo) > 0:
            promedio_bajo = promedio(grupo_bajo)
        else:
            promedio_bajo = 0

        if len(grupo_alto) > 0:
            promedio_alto = promedio(grupo_alto)
        else:
            promedio_alto = 0

        filas.append(
            {
                "parametro": nombre,
                "promedio_grupo_bajo": promedio_bajo,
                "promedio_grupo_alto": promedio_alto,
                "diferencia": promedio_alto - promedio_bajo,
            }
        )

    return filas
