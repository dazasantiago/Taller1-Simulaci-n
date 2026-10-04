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
con el mismo formato) y se guarda. En **Ejecución** se corre el estudio completo
(dos tandas de simulaciones: sin y con vacunación). En **Resultados** y
**Sensibilidad** aparecen las gráficas y tablas.

## Resultados del estudio completo

El estudio de 1.000 simulaciones por escenario (sin y con vacunación) ya se corrió
con `correr_estudio_completo.py` (semilla base 12345, una semilla distinta por
corrida). Tardó 1540 segundos (~25.7 minutos) con población completa (10.000,
365 días). Las gráficas, la tabla de estadísticas y los resultados crudos quedaron en
`outputs/` (ver `resumen_estudio.json` para las cifras exactas). Ese estudio es la
base del informe en Word.

Para reproducirlo:

```bash
python correr_estudio_completo.py
```

## Decisiones de modelado que hay que poder explicar

- **Fórmula de contactos.** El enunciado original tenía un error de coma: con
  `β ∈ [0.3, 0.5]` la fórmula `contactos = piso(r_contactos × β)` daba siempre 0
  (el producto nunca llega a 1). El profesor confirmó que el rango correcto es
  **β ∈ [3, 5]**, no [0.3, 0.5] — con eso la fórmula literal del enunciado funciona
  normal (`piso(r_contactos × β)` da entre 0 y 4 contactos por día). Implementado tal
  cual en `src/contagio.py::generar_numero_contactos` y `src/configuracion.py` (`RANGO_BETA`).
- **Muertes.** El profesor confirmó agregar una tasa de mortalidad/letalidad
  (`tasa_mortalidad`), típicamente U(0.01, 0.05) pero ajustable según la enfermedad
  que se quiera modelar. Se sortea una vez por simulación como los demás parámetros.
  Cuando un infectado pasa a Removido, se sortea si fallece (`r < tasa_mortalidad`) o
  se recupera; `total_muertes` y `total_recuperados` se reportan por separado además
  del total de Removidos (ver `src/progresion.py::avanzar_infectados` y
  `src/poblacion.py::contar_fallecidos`).
- **Parámetros por corrida.** β, σ⁻¹, γ⁻¹, p, tasa de vacunación, efectividad y tasa
  de mortalidad se sortean una vez al inicio de cada simulación (no por individuo) y
  se usan iguales para todos los que se expongan/infecten/mueran en esa corrida. σ⁻¹ y
  γ⁻¹ se redondean a días enteros (mínimo 1 día).
- **Selección del contacto.** Se arma la lista de índices susceptibles cada día y se
  elige uno al azar de esa lista (no de toda la población), tal como pide el
  enunciado.
- **Efecto de la vacuna.** Si el susceptible elegido está vacunado,
  `p_efectiva = p_base × (1 − efectividad_vacuna)`; si no, `p_efectiva = p_base`.
- **Análisis de sensibilidad.** Como cada una de las simulaciones sortea sus propios
  β/p/tasa de vacunación/tasa de mortalidad, se separan las corridas en mitad "valor
  bajo" / mitad "valor alto" por cada parámetro (según la mediana) y se compara el
  promedio de la métrica elegida (total de infectados o total de muertes) entre los
  dos grupos. Es el método detrás del gráfico tornado; la pestaña de Sensibilidad deja
  elegir cuál de las dos métricas mirar.

## Generador de números pseudoaleatorios: TEMPORAL

`src/generadores/generador_temporal.py` es un generador congruencial simple
**hecho solo para poder probar este punto mientras el módulo de
`punto 3 - generadores` no esté implementado** (`congruencial.py`,
`cuadrados_medios.py` y `distribuciones.py` siguen siendo placeholders vacíos).

Ese archivo está en `.gitignore` (no se sube al repositorio) porque es un parche
temporal, no parte del entregable. **Cuando el equipo termine el módulo de
generadores del Punto 3:**

1. Borrar `src/generadores/generador_temporal.py`.
2. Reemplazar los `import` de `generador_temporal` en `app/tab_ejecucion.py` (y
   cualquier script nuevo que lo use) por `generar_uniforme` de
   `punto 3 - generadores/src/generadores/distribuciones.py`.
3. Documentar en el informe qué método de generación (Cuadrados Medios,
   Congruencial, etc.) se usó, como pide el enunciado.

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
  generadores/generador_temporal.py   TEMPORAL, ver sección de arriba
  configuracion.py      parámetros por defecto y carga desde CSV
  poblacion.py          estados S/E/I/R y creación de la población
  contagio.py           número de contactos, elegir susceptible, evaluar transmisión
  progresion.py         E→I, I→R por conteo de días
  simulacion.py         una simulación completa (365 días)
  estudio.py            muchas simulaciones, bandas de confianza, sensibilidad
  graficas.py           las 8 funciones de gráficos (todas devuelven una Figure)
configuracion_ejemplo.csv
```

## Estado actual

- [x] Mecánica de contagio día a día (contactos, transmisión, vacunación, mortalidad).
- [x] Motor de una simulación completa y de un estudio de N simulaciones.
- [x] 9 gráficas (curva epidémica, 5 histogramas, comparación de escenarios, 2 tornado)
      y tabla de estadísticas descriptivas (incluye muertes).
- [x] Interfaz Streamlit con las 4 pestañas.
- [x] Fórmula de contactos y tratamiento de muertes confirmados con el profesor.
- [x] Estudio completo de 1.000 simulaciones corrido (ver `outputs/`).
- [ ] Conectar con los generadores reales del Punto 3 cuando estén implementados.

## Nota sobre uso de herramientas de IA

Este punto se desarrolló con asistencia de Claude Code (Anthropic) como asistente de
programación, bajo supervisión y dirección del estudiante en cada decisión técnica:
interpretación de la mecánica estocástica del enunciado, corrección de la fórmula de
contactos y del rango de β (confirmados con el profesor), definición de qué parámetros
se sortean por corrida, diseño del generador temporal mientras el módulo compartido de
Punto 3 no estaba listo, y validación de resultados (invariantes S+E+I+R=N, coherencia
de las cifras de mortalidad, comportamiento esperado al comparar escenarios).
