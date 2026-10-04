def generar_numero_contactos(beta, generador):
    r_contactos = generador()
    return int(r_contactos * beta)


def elegir_susceptible(lista_susceptibles, generador):
    r = generador()
    indice = int(r * len(lista_susceptibles))
    if indice >= len(lista_susceptibles):
        indice = len(lista_susceptibles) - 1
    return lista_susceptibles[indice]


def evaluar_transmision(p_base, efectividad_vacuna, vacunado, generador):
    if vacunado:
        p_efectiva = p_base * (1 - efectividad_vacuna)
    else:
        p_efectiva = p_base

    r_transmision = generador()
    return r_transmision < p_efectiva
