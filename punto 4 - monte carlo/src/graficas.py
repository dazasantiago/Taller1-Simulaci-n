import matplotlib.pyplot as plt

COLORES_ESTADOS = {"S": "tab:blue", "E": "tab:orange", "I": "tab:red", "R": "tab:green"}
ETIQUETAS_ESTADOS = {"S": "Susceptibles", "E": "Expuestos", "I": "Infectados", "R": "Removidos"}


def graficar_curva_epidemica(dias, curvas):
    fig, ax = plt.subplots()
    for nombre in ("S", "E", "I", "R"):
        curva_promedio, percentil_bajo, percentil_alto = curvas[nombre]
        color = COLORES_ESTADOS[nombre]
        ax.plot(dias, curva_promedio, label=ETIQUETAS_ESTADOS[nombre], color=color)
        ax.fill_between(dias, percentil_bajo, percentil_alto, color=color, alpha=0.2)

    ax.set_xlabel("Día")
    ax.set_ylabel("Personas")
    ax.set_title("Curva epidémica promedio con banda de confianza 95%")
    ax.legend()
    return fig


def graficar_histograma(valores, titulo, etiqueta_x):
    fig, ax = plt.subplots()
    ax.hist(valores, bins=20)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel("Cantidad de simulaciones")
    ax.set_title(titulo)
    return fig


def graficar_comparacion_escenarios(dias, curva_sin_vacunacion, curva_con_vacunacion):
    fig, ax = plt.subplots()
    ax.plot(dias, curva_sin_vacunacion, label="Sin vacunación", color="tab:red")
    ax.plot(dias, curva_con_vacunacion, label="Con vacunación", color="tab:green")
    ax.set_xlabel("Día")
    ax.set_ylabel("Infectados")
    ax.set_title("Comparación de escenarios: infectados promedio por día")
    ax.legend()
    return fig


def graficar_tornado(filas_sensibilidad):
    nombres = []
    diferencias = []
    for fila in filas_sensibilidad:
        nombres.append(fila["parametro"])
        diferencias.append(fila["diferencia"])

    posiciones = list(range(len(nombres)))

    fig, ax = plt.subplots()
    ax.barh(posiciones, diferencias)
    ax.set_yticks(posiciones)
    ax.set_yticklabels(nombres)
    ax.set_xlabel("Diferencia en infectados totales (grupo alto - grupo bajo)")
    ax.set_title("Análisis de sensibilidad")
    return fig
