# Punto 4 — EpiSim (Montecarlo SEIR)

Simulación Montecarlo de propagación de una enfermedad en una población de 10.000
personas (modelo SEIR modificado: Susceptible, Expuesto, Infectado, Removido), con
mecánica estocástica día a día y comparación de escenarios con y sin vacunación.

## Cómo correrla

Con el entorno virtual de la raíz del repositorio activado:

```bash
streamlit run app/main.py
```

Desde la pestaña **Configuración** se carga `configuracion_ejemplo.csv` (o uno propio
con el mismo formato) y se guarda. En **Ejecución** se corre el estudio completo (dos
tandas de simulaciones: sin y con vacunación, cada una con una semilla distinta). En
**Resultados** y **Sensibilidad** aparecen las gráficas y tablas.

Para reproducir el estudio completo sin pasar por la interfaz:

```bash
python correr_estudio_completo.py
```

Guarda las figuras, la tabla de resultados y los resultados crudos en `outputs/`.

## Modelo

Cada simulación sortea, una única vez, los siguientes parámetros:

| Parámetro | Distribución |
|---|---|
| Tasa de contacto (β) | U(3, 5) |
| Período de incubación (σ⁻¹, días) | U(2, 5) |
| Período infeccioso (γ⁻¹, días) | U(7, 14) |
| Probabilidad de transmisión (p) | U(0.4, 0.6) |
| Tasa de vacunación | U(0.3, 0.7) |
| Efectividad de la vacuna | U(0.80, 0.95) |
| Tasa de mortalidad | U(0.01, 0.05) |

σ⁻¹ y γ⁻¹ se redondean a días enteros (mínimo 1) y se aplican por igual a todos los
individuos que se expongan/infecten en esa corrida.

Mecánica diaria:

1. Cada infectado genera `r ~ U(0,1)` y obtiene `piso(r × β)` contactos ese día.
2. Cada contacto elige un susceptible al azar de la lista de susceptibles vigentes.
3. La probabilidad de transmisión es `p` si el susceptible no está vacunado, o
   `p × (1 − efectividad_vacuna)` si lo está.
4. Los expuestos pasan a infectados tras el período de incubación; los infectados
   pasan a removidos tras el período infeccioso, sorteando en ese momento si el
   individuo fallece (con probabilidad igual a la tasa de mortalidad) o se recupera.

El análisis de sensibilidad separa las corridas de un estudio en dos grupos por cada
parámetro (por encima/por debajo de la mediana de ese parámetro) y compara el
promedio de la métrica elegida (total de infectados o total de muertes) entre ambos
grupos; la diferencia es la barra del gráfico de tornado.

## Generación de números pseudoaleatorios

`src/generador_adaptador.py` (`GeneradorMonteCarlo`) conecta el modelo directamente
con el generador congruencial lineal de `punto 3 - generadores/src/generadores/congruencial.py`:
genera los enteros en lotes (5.000 a la vez), los normaliza a [0, 1) con
`uniforme_desde_enteros` y entrega un valor a la vez a través de
`siguiente_uniforme()`. Cada simulación del estudio se instancia con su propia
semilla (`semilla_base + i`), por lo que las 1.000 corridas de cada escenario son
independientes entre sí.

## Resultados del estudio completo

Estudio de 1.000 simulaciones por escenario (sin y con vacunación), población
completa (10.000, 365 días), generador conectado a Punto 3. Resultados y gráficas en
`outputs/`; el informe completo con la interpretación está en
`Informe_Punto4_EpiSim.docx`.

## Estructura

```
app/
  main.py               entrada (streamlit run app/main.py), arma las 4 pestañas
  estado.py             memoria de la sesión (st.session_state)
  tab_configuracion.py  cargar/editar parámetros, semilla, n° de simulaciones
  tab_ejecucion.py      corre el estudio (sin y con vacunación) con barra de progreso
  tab_resultados.py     curva epidémica, histogramas, comparación, tabla
  tab_sensibilidad.py   gráfico tornado y tabla de sensibilidad
src/
  generador_adaptador.py   conecta con el generador real de Punto 3
  configuracion.py      parámetros por defecto y carga desde CSV
  poblacion.py          estados S/E/I/R y creación de la población
  contagio.py           número de contactos, elegir susceptible, evaluar transmisión
  progresion.py         E→I, I→R por conteo de días, con sorteo de mortalidad
  simulacion.py         una simulación completa (365 días)
  estudio.py            muchas simulaciones, bandas de confianza, sensibilidad
  graficas.py           las 9 funciones de gráficos (todas devuelven una Figure)
correr_estudio_completo.py   script para reproducir el estudio completo sin la UI
configuracion_ejemplo.csv
```

## Estado actual

- [x] Mecánica de contagio día a día (contactos, transmisión, vacunación, mortalidad).
- [x] Motor de una simulación completa y de un estudio de N simulaciones.
- [x] 9 gráficas (curva epidémica, 5 histogramas, comparación de escenarios, 2 tornado)
      y tabla de estadísticas descriptivas (incluye muertes).
- [x] Interfaz Streamlit con las 4 pestañas.
- [x] Conectado al generador real de Punto 3 (`generador_adaptador.py`).
- [x] Estudio completo de 1.000 simulaciones corrido (ver `outputs/`).

## Nota sobre el uso de herramientas de inteligencia artificial

Claude (Anthropic) ayudó en el desarrollo de la interfaz Streamlit de este punto
(las 4 pestañas y el manejo de sesión) y en
parte de la documentación técnica (este README).
