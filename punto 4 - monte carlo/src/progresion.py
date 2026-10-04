from src import poblacion


def avanzar_infectados(estado, dias_restantes, fallecido, tasa_mortalidad, generador):
    for i in range(len(estado)):
        if estado[i] == poblacion.ESTADO_INFECTADO:
            dias_restantes[i] -= 1
            if dias_restantes[i] <= 0:
                estado[i] = poblacion.ESTADO_REMOVIDO
                dias_restantes[i] = 0
                r_mortalidad = generador()
                if r_mortalidad < tasa_mortalidad:
                    fallecido[i] = True


def avanzar_expuestos(estado, dias_restantes, dias_infeccioso):
    for i in range(len(estado)):
        if estado[i] == poblacion.ESTADO_EXPUESTO:
            dias_restantes[i] -= 1
            if dias_restantes[i] <= 0:
                estado[i] = poblacion.ESTADO_INFECTADO
                dias_restantes[i] = dias_infeccioso


def aplicar_nuevos_expuestos(estado, dias_restantes, indices_nuevos_expuestos, dias_incubacion):
    for indice in indices_nuevos_expuestos:
        if estado[indice] == poblacion.ESTADO_SUSCEPTIBLE:
            estado[indice] = poblacion.ESTADO_EXPUESTO
            dias_restantes[indice] = dias_incubacion
