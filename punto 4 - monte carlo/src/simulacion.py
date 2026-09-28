from src import contagio, poblacion, progresion


def sortear_parametro(rango, generador):
    minimo, maximo = rango
    r = generador()
    return minimo + r * (maximo - minimo)


def sortear_parametros(configuracion, generador):
    beta = sortear_parametro(configuracion["rango_beta"], generador)
    dias_incubacion = round(sortear_parametro(configuracion["rango_sigma"], generador))
    dias_infeccioso = round(sortear_parametro(configuracion["rango_gamma"], generador))
    p_transmision = sortear_parametro(configuracion["rango_p_transmision"], generador)
    tasa_vacunacion = sortear_parametro(configuracion["rango_tasa_vacunacion"], generador)
    efectividad_vacuna = sortear_parametro(configuracion["rango_efectividad_vacuna"], generador)

    if dias_incubacion < 1:
        dias_incubacion = 1
    if dias_infeccioso < 1:
        dias_infeccioso = 1

    return {
        "beta": beta,
        "dias_incubacion": dias_incubacion,
        "dias_infeccioso": dias_infeccioso,
        "p_transmision": p_transmision,
        "tasa_vacunacion": tasa_vacunacion,
        "efectividad_vacuna": efectividad_vacuna,
    }


def correr_una_simulacion(configuracion, generador, forzar_sin_vacunacion=False):
    parametros = sortear_parametros(configuracion, generador)
    if forzar_sin_vacunacion:
        parametros["tasa_vacunacion"] = 0.0

    n_poblacion = configuracion["n_poblacion"]
    dias_simulacion = configuracion["dias_simulacion"]

    estado, dias_restantes, vacunado = poblacion.crear_poblacion(
        n_poblacion,
        configuracion["infectados_iniciales"],
        parametros["tasa_vacunacion"],
        parametros["dias_infeccioso"],
        generador,
    )

    historial_s = []
    historial_e = []
    historial_i = []
    historial_r = []

    for _ in range(dias_simulacion):
        susceptibles = []
        for i in range(n_poblacion):
            if estado[i] == poblacion.ESTADO_SUSCEPTIBLE:
                susceptibles.append(i)

        nuevos_expuestos = []
        if len(susceptibles) > 0:
            for i in range(n_poblacion):
                if estado[i] == poblacion.ESTADO_INFECTADO:
                    numero_contactos = contagio.generar_numero_contactos(parametros["beta"], generador)
                    for _ in range(numero_contactos):
                        if len(susceptibles) == 0:
                            break
                        indice_contacto = contagio.elegir_susceptible(susceptibles, generador)
                        hay_contagio = contagio.evaluar_transmision(
                            parametros["p_transmision"],
                            parametros["efectividad_vacuna"],
                            vacunado[indice_contacto],
                            generador,
                        )
                        if hay_contagio:
                            nuevos_expuestos.append(indice_contacto)

        progresion.avanzar_infectados(estado, dias_restantes)
        progresion.avanzar_expuestos(estado, dias_restantes, parametros["dias_infeccioso"])
        progresion.aplicar_nuevos_expuestos(estado, dias_restantes, nuevos_expuestos, parametros["dias_incubacion"])

        conteo_s, conteo_e, conteo_i, conteo_r = poblacion.contar_estados(estado)
        historial_s.append(conteo_s)
        historial_e.append(conteo_e)
        historial_i.append(conteo_i)
        historial_r.append(conteo_r)

    return resumir_simulacion(historial_s, historial_e, historial_i, historial_r, parametros, n_poblacion)


def resumir_simulacion(historial_s, historial_e, historial_i, historial_r, parametros, n_poblacion):
    dias_simulacion = len(historial_i)

    dia_pico = 0
    magnitud_pico = historial_i[0]
    for dia in range(dias_simulacion):
        if historial_i[dia] > magnitud_pico:
            magnitud_pico = historial_i[dia]
            dia_pico = dia

    total_infectados = n_poblacion - historial_s[dias_simulacion - 1]

    dias_hasta_control = None
    for dia in range(dia_pico, dias_simulacion):
        if historial_i[dia] == 0:
            dias_hasta_control = dia
            break

    return {
        "historial_s": historial_s,
        "historial_e": historial_e,
        "historial_i": historial_i,
        "historial_r": historial_r,
        "dia_pico": dia_pico,
        "magnitud_pico": magnitud_pico,
        "total_infectados": total_infectados,
        "dias_hasta_control": dias_hasta_control,
        "parametros": parametros,
    }
