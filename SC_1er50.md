# Taller Primer 50%

**Simulación por computador**
Universidad Pedagógica y Tecnológica de Colombia

## Números pseudoaleatorios, caminatas aleatorias y método Montecarlo

### Fundamentos del Aprendizaje y Propósito

Este taller integra los contenidos de las Unidades 1 y 2 del curso mediante cuatro problemas de ingeniería que requieren análisis crítico de números pseudoaleatorios, diseño de generadores válidos, construcción e implementación de modelos de simulación basados en caminatas aleatorias y Montecarlo, evaluación estadística de resultados, y síntesis de conclusiones fundamentadas en análisis de validación.

El objetivo no es entregar simulaciones preconstruidas, sino construir comprensión mediante el esfuerzo riguroso de pensar en la naturaleza del fenómeno, seleccionar técnicas apropiadas, implementar algoritmos, experimentar con parámetros y evaluar la confiabilidad de resultados.

El aprendizaje genuino emerge del trabajo consciente y autónomo. Cada decisión sobre el generador de pseudoaleatorios, cada prueba estadística aplicada, cada implementación de la lógica de simulación, cada análisis de convergencia de resultados y cada interpretación de salidas representan oportunidades de crecimiento real. Los trabajos que reflejan esfuerzo propio, argumentación técnica clara y validación rigurosa de modelos evidencian ese crecimiento. Si se utiliza colaboración de herramientas de inteligencia artificial (modelos de lenguaje, asistentes de código, librerías de simulación, etc.), debe aclararse explícitamente cuál fue su rol, qué partes fueron desarrolladas de forma independiente y qué decisiones técnicas fueron tomadas por el estudiante, permitiendo que el docente evalúe la calidad del aprendizaje alcanzado.

### Requerimientos del Taller

Cada punto requiere:

- Generación e implementación de números pseudoaleatorios (código del generador, documentación del método).
- Pruebas de validación estadística (pruebas de uniformidad, independencia, periodicidad).
- Formalización del problema de simulación (definición de variables de estado, parámetros, eventos).
- Diseño e implementación del modelo (lógica de simulación documentada, manejo de aleatoriedad).
- Métricas de evaluación de resultados (inicialización → generación de números → ejecución de eventos → recolección de datos → análisis).
- Evidencia visual (gráficos de distribuciones, trazas de simulación, histogramas de resultados, pantallazos de ejecución, salidas en consola, notebooks documentados).

Los análisis deben incluir interpretación clara de resultados, validación estadística de la confiabilidad del modelo, limitaciones de la simulación y recomendaciones técnicas.

### Resultado de Aprendizaje

Implementa sistemas de simulación completos que integren números pseudoaleatorios validados y modelos matemáticos coherentes, demostrando capacidad para analizar fenómenos de sistemas reales y proporcionar análisis aplicables a la solución de problemas organizacionales y científicos.

### Competencias relacionadas a la actividad

- Genera números pseudoaleatorios mediante técnicas estadísticas y matemáticas para garantizar la confiabilidad de datos de entrada en programas de simulación.
- Desarrolla modelos de simulación con números pseudoaleatorios que reproduzcan el comportamiento de sistemas complejos y faciliten la evaluación de alternativas en contextos de toma de decisiones.

---

## 1. Presentación del Informe (Valor: 0.5)

### 1.1. Estructura y Formato (IEEE)

- Portada: título, autores, institución, fecha, código de curso.
- Contraportada: resumen ejecutivo (máx. 150 palabras).
- Tabla de contenido con números de página.
- Lista de figuras y tablas (si aplica).
- Numeración continua de páginas.
- Márgenes: 2.5 cm (superior/inferior), 3 cm (izquierda/derecha).
- Fuente: Times New Roman 12 pt (cuerpo), 10 pt (pie de página).
- Interlineado: 1.5.
- Máximo 40 páginas (sin incluir anexos).

### 1.2. Componentes Técnicos

- **Introducción:** contexto del problema, objetivos, alcance.
- **Desarrollo:** secciones numeradas (1., 1.1, 1.2, 2., 2.1, etc.).
- **Resultados:** presentación sistemática de hallazgos.
- **Análisis:** interpretación técnica rigurosa (NO descriptiva).
- **Conclusiones:** redactadas en párrafos coherentes que sinteticen aprendizajes, reflexionen sobre implicaciones técnicas, y eviten repetir resultados. Mínimo 2 párrafos, máximo 4. Lenguaje profesional sin coloquialismos.
- **Referencias bibliográficas:** mínimo 5, formato IEEE.

### 1.3. Figuras y Tablas

- Todas numeradas consecutivamente y con título descriptivo.
- Título de tabla: encima (Tabla 1: Descripción...); pie de figura: debajo (Figura 3: Descripción...).
- Referenciadas explícitamente en el texto ("ver Tabla 1", "según se observa en la Figura 3").
- Fuente legible, contraste adecuado.
- Diagramas con etiquetas, leyendas claras.

### 1.4. Lenguaje Técnico

- Tono impersonal y formal (se diseñó, se implementó, NO "yo hice", "nosotros hicimos").
- Vocabulario preciso y especializado.
- Párrafos bien estructurados con tema central claro.
- Evitar: "cositas", "muy", "bastante", "chungo", diminutivos, expresiones coloquiales.
- Cada afirmación teórica debe estar citada.
- Transiciones claras entre párrafos.

### 1.5. Ortografía y Gramática

- Cero faltas de ortografía permitidas (acentos, mayúsculas, signos de puntuación).
- Concordancia gramatical: género, número, tiempos verbales.
- Puntuación correcta (comas, puntos, punto y coma).
- Verificar con herramientas (Grammarly, revisor de Word) como mínimo.
- **Una falta ortográfica = descalificación del punto.**

### Criterio de evaluación — Presentación del Informe (Valor: 0.5)

El informe se encuentra en formato PDF con estructura IEEE (portada, contraportada, tabla de contenido, numeración continua de páginas), márgenes 2.5 cm superior/inferior y 3 cm laterales, fuente Times New Roman 12 pt a interlineado 1.5. Contiene pies de página, diagramación profesional, citas y referencias bibliográficas según norma IEEE (mínimo 5). Todas las figuras y tablas están numeradas con título descriptivo y referenciadas explícitamente en el texto. El lenguaje es técnico, impersonal y preciso, evitando coloquialismos. Ortografía, acentuación y puntuación sin errores. Las conclusiones están redactadas en 2-4 párrafos coherentes que sintetizan aprendizajes técnicos sin repetir resultados. Máximo 40 páginas sin incluir anexos.

**Total Punto 1: 0.5**

---

## 2. La rana estadística en mundos paralelos: simulación y análisis multidimensional de caminatas aleatorias (Valor: 1.0)

Había una vez una rana que, con un sentido perfecto de la simetría y la estadística, se sentaba en el origen de una recta numérica infinita. Esta rana podía brincar hacia adelante o hacia atrás, en pasos de una unidad, con idéntica probabilidad. Pero un día, la rana se cansó de su mundo unidimensional y decidió explorar también el plano y el espacio tridimensional.

### Análisis probabilístico inicial

- Determinen la probabilidad de que la rana retorne al origen exactamente después de 2, 3 y 4 saltos.
- Generalicen para un número par y un número impar de saltos: ¿qué se puede afirmar sobre la probabilidad de retorno al origen en cada caso?

### Estrategia computacional para grandes cantidades de pasos

- Propongan y justifiquen una estrategia para estimar la posición más probable de la rana después de 1.000.000 de saltos.
- Relacionen la estrategia con el comportamiento límite de las caminatas aleatorias simétricas, y vincúlenlo con la Ley de los Grandes Números o el Teorema Central del Límite.

### Simulación computacional unidimensional

- Implementen un programa que simule el comportamiento de la rana hasta el millonésimo salto en una dimensión.
- El programa debe permitir modificar la semilla del generador aleatorio y replicar múltiples simulaciones independientes (al menos 100).

### Visualización y análisis de resultados en 1D

- Generen un histograma de frecuencias que muestre las posiciones finales de la rana tras las múltiples simulaciones. ¿Qué forma tiene? ¿Por qué?
- Analicen la dispersión, la simetría del resultado y su relación con distribuciones estadísticas conocidas.

### Extensión multidimensional del problema

- Reformulen el programa anterior para simular el movimiento de la rana en dos dimensiones y luego en tres dimensiones.
- Ejecuten al menos 100 simulaciones independientes en cada dimensión (2D y 3D), con 1.000.000 de pasos por simulación.
- Estimen la probabilidad de retorno al origen tras 1.000 pasos en cada dimensión (1D, 2D, 3D).
- Comparen e interpreten estos resultados considerando la naturaleza del problema en espacios de diferente dimensionalidad.
- Justifiquen y seleccionen representaciones visuales apropiadas para 2D (ej: scatter plot, heatmap) y 3D (ej: scatter 3D, proyecciones ortogonales). ¿Por qué cada visualización es adecuada para interpretar el comportamiento en cada dimensión?
- Midan y reporten los tiempos de ejecución y eficiencia computacional del algoritmo en las tres dimensiones.

### Discusión computacional

- Argumenten, con base en literatura matemática, por qué el comportamiento de retorno al origen cambia significativamente entre 1D, 2D y 3D. ¿Qué implicaciones tiene esto para modelar fenómenos físicos reales (difusión de partículas, movimiento de moléculas, etc.)?
- Incluyan al menos dos referencias formales (libros o artículos) que respalden su análisis.

### Entregables

- Código fuente funcional, estructurado y comentado en el lenguaje de programación seleccionado.
- Documentación técnica del código (comentarios en línea, explicación de funciones principales y estructuras de datos utilizadas).
- Cuadro comparativo de eficiencia computacional con tiempos de ejecución, memoria utilizada y análisis de escalabilidad entre dimensiones (1D, 2D, 3D).
- Evidencia de ejecución: pantallazos de salidas en consola, histogramas, gráficos de trayectorias y scatter plots generados.
- Presentación y sustentación del trabajo ante el grupo para discusión de resultados, decisiones técnicas y validación de modelos.

### Criterio de evaluación — La rana estadística (Valor: 1.0)

La evaluación del punto se basará en los siguientes criterios: claridad y precisión en la formulación matemática de las caminatas aleatorias y validación de números pseudoaleatorios mediante pruebas estadísticas, implementación correcta y replicable del programa de simulación, análisis de escalabilidad computacional incluyendo tiempos de ejecución y uso de memoria entre dimensiones (1D, 2D, 3D), calidad y pertinencia de las visualizaciones generadas, profundidad en el análisis estadístico y conceptual de los resultados obtenidos, argumentación teórica sustentada en fuentes bibliográficas confiables, y claridad en la presentación y sustentación oral del trabajo. Cada uno de estos aspectos será valorado de forma equilibrada, considerando tanto la solidez del contenido como la rigurosidad de la argumentación.

**Total Punto 2: 1.0**

---

## 3. Construcción y validación de generadores de números pseudoaleatorios (Valor: 1.5)

Como parte del desarrollo de modelos de simulación, es imprescindible construir generadores de números pseudoaleatorios, **desde cero**, que sean sistemáticos, comprensibles y reutilizables como bibliotecas en trabajos posteriores. Se solicita la creación de un módulo integrado que implemente y compare los siguientes métodos de generación:

- Método de los Cuadrados Medios.
- Métodos Congruenciales (lineal, aditivo y multiplicativo).
- Métodos basados en distribuciones uniforme y normal (vía transformación).

Y que permita someter las secuencias generadas a validación mediante las siguientes pruebas estadísticas:

- Prueba de medias.
- Prueba de varianza.
- Prueba Chi-cuadrado.
- Prueba de Kolmogorov-Smirnov (KS).
- Prueba de Póker.
- Prueba de rachas (runs test).

### Requisitos técnicos y funcionales

#### Implementación desde cero (from scratch)

- Los algoritmos deben implementarse manualmente sin utilizar librerías de generación de números aleatorios del lenguaje de programación (`numpy.random`, `random`, etc.). Esto es crítico para demostrar comprensión de los métodos y garantizar que el módulo sea educativamente riguroso.
- Tampoco se permite el uso de prompts a herramientas de inteligencia artificial para generar el algoritmo completo. Se espera trabajo autónomo y fundamentado.
- Cada algoritmo debe estar claramente separado, modularizado y documentado internamente.

#### Interfaz funcional

- El sistema debe aceptar entrada de semillas desde archivo plano (.txt, .csv) y permitir ingreso manual.
- Permitir seleccionar qué método(s) de generación utilizar.
- Permitir seleccionar qué prueba(s) de validación ejecutar.
- Visualizar secuencias generadas en tablas exportables.

### Visualización de resultados

#### Generación de números

- Histogramas de frecuencias para cada método de generación (Cuadrados Medios, Congruenciales lineal/aditivo/multiplicativo, Uniforme, Normal) mostrando claramente la distribución alcanzada.

#### Validación: pruebas y gráficos

- **Prueba de medias:** gráfico que muestre la distribución de las medias calculadas, los intervalos de confianza generados, y marcar la media teórica esperada.
- **Prueba de varianza:** gráfico que muestre la distribución de varianzas, intervalos de confianza y varianza teórica esperada.
- **Prueba Chi-cuadrado:** gráfico de barras comparando frecuencias observadas vs frecuencias esperadas (uniformidad), visualizando inmediatamente el ajuste a la distribución uniforme.
- **Prueba Kolmogorov-Smirnov (KS):** gráfico de la función empírica acumulada (FEC) vs distribución teórica uniforme, destacando la máxima diferencia (estadístico D).
- **Prueba de Póker:** histograma de las "manos" (patrones de dígitos) observadas vs esperadas, similar a Chi-cuadrado pero para patrones.
- **Prueba de rachas:** gráfico de barras mostrando cantidad de rachas observadas vs cantidad esperada con su intervalo de confianza.

#### Diseño modular reutilizable

- El sistema debe estar estructurado como biblioteca que integre generadores y validadores para uso en futuros trabajos de simulación.
- Documentación interna mínima: comentarios claros, nombres de funciones descriptivos, instrucciones de uso básicas en archivo README.

### Entregables

- Código fuente funcional, estructurado y comentado en lenguaje de programación seleccionado.
- Documentación técnica del módulo (archivo README con descripción de cada función, parámetros y uso).
- Cuadro técnico con lenguaje de programación, sistema operativo, procesador y memoria.
- Evidencia de ejecución: capturas de pantalla mostrando histogramas de generación, carga de archivos externos, y resultados gráficos de al menos una prueba estadística completa.
- Archivo de ejemplo (.txt o .csv) con semillas para demostrar carga externa.

### Criterio de evaluación — Generadores (Valor: 1.5)

La evaluación considerará la implementación correcta y desde cero de cada método de generación, la claridad y modularidad del código facilitando su reutilización, la implementación completa de las seis pruebas estadísticas, la calidad y pertinencia de las visualizaciones generadas según los requisitos, la correcta interpretación estadística de los resultados, la documentación técnica del módulo, y la presentación general del código. Se valorará especialmente que no se haya recurrido a librerías de generación de números aleatorios ni a herramientas de IA para implementación de algoritmos, demostrando comprensión profunda de los métodos.

**Total Punto 3: 1.5**

---

## 4. EpiSim - Simulación Montecarlo de propagación de enfermedades contagiosas (Valor: 2.0)

La modelación matemática de la propagación de enfermedades contagiosas es una herramienta crítica en salud pública para entender dinámicas de transmisión, evaluar impacto de intervenciones y diseñar estrategias de contención. Se solicita implementar una simulación Montecarlo que modele la propagación de una enfermedad en una población heterogénea bajo condiciones estocásticas controladas, utilizando números pseudoaleatorios para representar la aleatoriedad inherente del proceso de contagio.

### Descripción del modelo (SEIR modificado)

Población con N individuos clasificados en estados:

- **S (Susceptibles):** pueden contagiarse.
- **E (Expuestos):** infectados pero aún no contagiosos.
- **I (Infectados):** contagiosos activos.
- **R (Recuperados/Removidos):** inmunes o fallecidos.

### Parámetros iniciales (generación pseudoaleatoria)

| Parámetro | Distribución | Descripción |
|---|---|---|
| Población inicial (N) | Fijo: 10.000 | Individuos en simulación |
| Infectados iniciales | Fijo: 10 | Casos índice |
| Tasa de contacto básico (β) | U(0.3, 0.5) | Promedio de contactos por día |
| Período de incubación (σ⁻¹) | U(2, 5) | Días en estado E |
| Período infeccioso (γ⁻¹) | U(7, 14) | Días en estado I |
| Probabilidad de transmisión (p) | U(0.4, 0.6) | Prob. de contagio si hay contacto |
| Tasa de vacunación | U(0.3, 0.7) | Proporción de población vacunada |
| Efectividad vacuna | U(0.80, 0.95) | Reducción de susceptibilidad |

### Mecánica de simulación estocástica (por día, 365 días × 1.000 simulaciones)

**Paso 1: Generación estocástica de contactos.** Cada día, para cada individuo infectado, se genera el número de contactos mediante un número pseudoaleatorio:

- Generar `r_contactos ~ U(0,1)`.
- Número de contactos = `piso(r_contactos × β_máximo)`.

Ejemplo: si β ~ U(0.3, 0.5) y `r_contactos` = 0.75, entonces contactos = piso(0.75 × 0.5) = 0 contactos.

**Paso 2: Selección estocástica de susceptibles.** Para cada contacto generado, seleccionar aleatoriamente UN individuo susceptible de la población.

**Paso 3: Evaluación estocástica de transmisión.** Para cada contacto establecido, determinar si hay contagio:

- Generar `r_transmisión ~ U(0,1)`.
- Calcular `p_transmisión_efectiva = p_base × factor_vacunación`.
- SI `r_transmisión < p_transmisión_efectiva` → el susceptible pasa a estado E.
- SI `r_transmisión ≥ p_transmisión_efectiva` → no hay contagio.

**Progresión de estados (determinística después de contagio):**

- E → I: después de período de incubación (pseudoaleatorio en días, sin más variabilidad).
- I → R: después de período infeccioso (pseudoaleatorio en días).

### Objetivos analíticos requeridos

- Curva epidémica completa (S, E, I, R en el tiempo) con valores promedio e intervalos de confianza.
- Distribución de picos (día de máximo I, magnitud).
- Total de infectados y muertes (estadísticas descriptivas).
- Impacto de vacunación: comparar escenarios sin vs con vacunación.
- Análisis de sensibilidad: ¿qué parámetro (β, p, vacunación) impacta más?
- Tiempo de simulación.

### Requisitos técnicos y funcionales

#### Generación de números pseudoaleatorios

- Utilizar el módulo de generadores y validadores de secuencias pseudoaleatorias desarrollado en Punto 2 (desde cero, from scratch).
- Documentar qué método de generación se utilizó para β, períodos de incubación y transmisión.

#### Implementación del modelo

- Arquitectura modular: funciones para generación de contactos, evaluación de transmisión, progresión de estados.
- Parametrización externa: permitir cargar parámetros desde archivo (.txt o .csv).
- Ejecutar 100 simulaciones independientes con semillas diferentes.

#### Visualización de resultados

- Gráfico de curvas epidémicas (línea promedio + banda de confianza al 95%).
- Histogramas: distribución de picos, total de infectados, días hasta control.
- Gráfico comparativo de escenarios: sin vacunación vs con vacunación.
- Análisis de sensibilidad en gráfico tornado o barras.
- Tabla de estadísticas descriptivas por escenario.

### Entregables

- Código fuente funcional, modularizado y comentado.
- Documentación técnica explicando el mecanismo estocástico, decisiones de parametrización e integración del módulo de números pseudoaleatorios.
- Cuadro técnico con especificaciones del equipo.
- Mínimo 6 gráficos de resultados con interpretación clara.
- Archivo de configuración con parámetros ajustables para diferentes escenarios.
- Análisis crítico: reflexión sobre limitaciones del modelo, validez de supuestos y posibles mejoras.

### Extensión de complejidad (opcional)

Los estudiantes que deseen mejorar su calificación en este punto pueden extender el modelo incorporando:

- Heterogeneidad por edad (diferentes tasas de transmisión y mortalidad).
- Múltiples variantes del virus con transmisibilidad variable.
- Dinámicas de comportamiento humano (cumplimiento variable de distanciamiento).
- Estructura espacial (geografía, movilidad entre regiones).
- Intervenciones más realistas (cuarentena, aislamiento, testeo).
- Modelado de sistemas de salud (capacidad hospitalaria, disponibilidad de recursos).

Cualquier extensión debe estar documentada, justificada teóricamente, y sus resultados deben analizarse críticamente.

### Criterio de evaluación — EpiSim (Valor: 2.0)

La evaluación considerará la implementación correcta del mecanismo estocástico descrito, la integración funcional del módulo de números pseudoaleatorios del Punto 2, la ejecución robusta de 1.000 simulaciones independientes, la precisión y claridad de las visualizaciones, la profundidad del análisis de sensibilidad y comparación de escenarios, la documentación técnica, y la reflexión crítica sobre limitaciones del modelo. Se valorará especialmente la demostración clara de cómo se generan y utilizan números pseudoaleatorios en cada paso del proceso de contagio. Adicionalmente, cualquier extensión de complejidad que agregue realismo al modelo será considerada favorablemente en la calificación final, siempre y cuando esté correctamente implementada y analizada.

**Total Punto 4: 2.0**

---

## Notas para la entrega

- Los laboratorios entregados fuera del tiempo establecido no serán tenidos en cuenta para calificación.
- Solo se calificarán trabajos entregados en la plataforma oficial de la universidad para esta clase de informes, para este caso es **Moodle**. Cualquier envío realizado a través de otros medios no se valorará en términos de su puntuación.
- Solo se calificarán trabajos que se encuentren totalmente diligenciados y resueltos, esto para poder evitar entregas incompletas.

Que se diviertan.

Att,
Alex :)

## Información general

| | |
|---|---|
| Tiempo de desarrollo | 6 semanas |
| Forma de trabajo | Cinco (5) grupos en total |

## Totales

| Punto 1 | Punto 2 | Punto 3 | Punto 4 | Total |
|---|---|---|---|---|
| 0.5 | 1.0 | 1.5 | 2.0 | 5.0 |
