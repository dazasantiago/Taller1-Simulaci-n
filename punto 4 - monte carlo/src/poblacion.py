ESTADO_SUSCEPTIBLE = "S"
ESTADO_EXPUESTO = "E"
ESTADO_INFECTADO = "I"
ESTADO_REMOVIDO = "R"


def crear_poblacion(n_poblacion, infectados_iniciales, tasa_vacunacion, dias_infeccioso, generador):
    estado = []
    for _ in range(n_poblacion):
        estado.append(ESTADO_SUSCEPTIBLE)

    dias_restantes = []
    for _ in range(n_poblacion):
        dias_restantes.append(0)

    vacunado = []
    for _ in range(n_poblacion):
        r = generador()
        vacunado.append(r < tasa_vacunacion)

    fallecido = []
    for _ in range(n_poblacion):
        fallecido.append(False)

    infectados_asignados = 0
    while infectados_asignados < infectados_iniciales:
        r = generador()
        indice = int(r * n_poblacion)
        if indice >= n_poblacion:
            indice = n_poblacion - 1
        if estado[indice] == ESTADO_SUSCEPTIBLE:
            estado[indice] = ESTADO_INFECTADO
            dias_restantes[indice] = dias_infeccioso
            infectados_asignados += 1

    return estado, dias_restantes, vacunado, fallecido


def contar_estados(estado):
    conteo_s = 0
    conteo_e = 0
    conteo_i = 0
    conteo_r = 0
    for valor in estado:
        if valor == ESTADO_SUSCEPTIBLE:
            conteo_s += 1
        elif valor == ESTADO_EXPUESTO:
            conteo_e += 1
        elif valor == ESTADO_INFECTADO:
            conteo_i += 1
        else:
            conteo_r += 1
    return conteo_s, conteo_e, conteo_i, conteo_r


def contar_fallecidos(fallecido):
    conteo = 0
    for valor in fallecido:
        if valor:
            conteo += 1
    return conteo
