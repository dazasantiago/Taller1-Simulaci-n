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

## Pendiente antes de correr el estudio completo

**No se ha corrido el estudio con 1.000 simulaciones todavía.** Hay una pregunta
abierta para el profesor sobre la mecánica de contactos (ver más abajo); hasta que
responda, conviene probar con pocas simulaciones (`n_simulaciones` bajo, ej. 10-20)
para no invertir tiempo de cómputo en un supuesto que puede cambiar.

## Decisiones de modelado que hay que poder explicar

- **Fórmula de contactos (⚠️ preguntar al profesor).** El enunciado dice
  `contactos = piso(r_contactos × β)`, con `r_contactos ~ U(0,1)` y `β ∈ [0.3, 0.5]`.
  Esa fórmula da **siempre 0** (el producto nunca llega a 1, así que `piso()` nunca
  sube de 0), lo que congelaría la epidemia en los infectados iniciales para siempre.
  Mientras se confirma con el profesor, `src/contagio.py::generar_numero_contactos`
  usa una interpretación temporal: cada día, cada infectado tiene 1 contacto si
  `r_contactos < β` (0 en caso contrario) — esto coincide con que la tabla de
  parámetros describe β como "promedio de contactos por día". Es la única función que
  hay que tocar si el profesor da otra fórmula.
- **Parámetros por corrida.** β, σ⁻¹, γ⁻¹, p, tasa de vacunación y efectividad se
  sortean una vez al inicio de cada simulación (no por individuo) y se usan iguales
  para todos los que se expongan/infecten en esa corrida. σ⁻¹ y γ⁻¹ se redondean a
  días enteros (mínimo 1 día).
- **Selección del contacto.** Se arma la lista de índices susceptibles cada día y se
  elige uno al azar de esa lista (no de toda la población), tal como pide el
  enunciado.
- **Efecto de la vacuna.** Si el susceptible elegido está vacunado,
  `p_efectiva = p_base × (1 − efectividad_vacuna)`; si no, `p_efectiva = p_base`.
- **Muertes.** El enunciado pide reportar "muertes", pero la tabla de parámetros no
  da ninguna tasa de mortalidad y define R como "inmunes o fallecidos" sin
  separarlos. No se inventó una tasa de letalidad: se reporta una sola categoría
  "Removidos". Vale la pena preguntarle esto al profesor junto con lo de los
  contactos.
- **Análisis de sensibilidad.** Como cada una de las simulaciones sortea sus propios
  β/p/tasa de vacunación, se separan las corridas en mitad "valor bajo" / mitad
  "valor alto" por cada parámetro (según la mediana) y se compara el promedio de
  infectados totales entre los dos grupos. Es el método detrás del gráfico tornado.

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
  graficas.py           las 7 funciones de gráficos (todas devuelven una Figure)
configuracion_ejemplo.csv
```

## Estado actual

- [x] Mecánica de contagio día a día (contactos, transmisión, vacunación).
- [x] Motor de una simulación completa y de un estudio de N simulaciones.
- [x] 7 gráficas (curva epidémica, 4 histogramas, comparación de escenarios, tornado)
      y tabla de estadísticas descriptivas.
- [x] Interfaz Streamlit con las 4 pestañas.
- [ ] Confirmar con el profesor la fórmula de contactos y el tratamiento de muertes.
- [ ] Correr el estudio completo de 1.000 simulaciones (queda pendiente a propósito).
- [ ] Conectar con los generadores reales del Punto 3 cuando estén implementados.
