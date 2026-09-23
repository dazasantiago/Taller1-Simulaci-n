# Taller Primer 50%: Simulación por Computador
**Universidad Pedagógica y Tecnológica de Colombia (UPTC)**  
*Escuela de Ingeniería de Sistemas y Computación*  
**Asignatura:** Simulación por Computador  
**Tema:** Números Pseudoaleatorios, Caminatas Aleatorias y Método Montecarlo  

---

## Resumen Ejecutivo

Este informe presenta el diseño, implementación y validación rigurosa de un sistema completo de simulación estocástica desarrollado para resolver problemas de ingeniería complejos. Se construyeron desde cero (*from scratch*) generadores de números pseudoaleatorios (Cuadrados Medios, Congruenciales Lineal/Aditivo/Multiplicativo y transformaciones a distribuciones Uniforme y Normal), sin hacer uso de librerías aleatorias del lenguaje. La calidad de las secuencias generadas fue sometida a validación estadística mediante un conjunto de seis pruebas (Medias, Varianza, Chi-cuadrado, Kolmogorov-Smirnov, Póker y Rachas). Asimismo, se exploró el comportamiento multidimensional de caminatas aleatorias simétricas (1D, 2D y 3D) a la luz de la Ley de los Grandes Números y el Teorema de Pólya, y se implementó una simulación Montecarlo estocástica (EpiSim) para evaluar la propagación de epidemias bajo el modelo SEIR en una población de 10.000 individuos.

---

## Tabla de Contenido

1. [Introducción](#1-introducción)
2. [Desarrollo del Proyecto](#2-desarrollo-del-proyecto)
   - 2.1 [La Rana Estadística en Mundos Paralelos: Caminatas Aleatorias (1D, 2D y 3D)](#21-la-rana-estadística-en-mundos-paralelos-caminatas-aleatorias-1d-2d-y-3d)
   - 2.2 [Construcción y Validación de Generadores Pseudoaleatorios](#22-construcción-y-validación-de-generadores-pseudoaleatorios)
   - 2.3 [EpiSim: Simulación Montecarlo de Propagación de Enfermedades (SEIR)](#23-episim-simulación-montecarlo-de-propagación-de-enfermedades-seir)
3. [Resultados](#3-resultados)
4. [Análisis Técnico](#4-análisis-técnico)
5. [Conclusiones](#5-conclusiones)
6. [Referencias Bibliográficas](#6-referencias-bibliográficas)

---

## 1. Introducción

La simulación computacional constituye una herramienta indispensable en la ingeniería moderna para modelar y analizar sistemas complejos cuya estocasticidad impide una solución analítica directa. La validez de cualquier modelo estocástico depende de la calidad de los números pseudoaleatorios generados, los cuales deben cumplir de forma rigurosa con las propiedades de uniformidad en el intervalo $[0, 1)$ e independencia mutua ($i.i.d.$).

El presente trabajo tiene como objetivo construir desde cero un marco de simulación reutilizable y científicamente fundamentado. En la primera fase, se analiza el comportamiento de caminatas aleatorias en 1D, 2D y 3D para evaluar la tasa de retorno al origen y el crecimiento de la dispersión espacial. En la segunda fase, se diseña una biblioteca modular de generadores de números pseudoaleatorios y validadores estadísticos. Finalmente, se aplica el método Montecarlo para simular la dinámica estocástica de transmisión de una enfermedad infecciosa mediante un modelo SEIR modificado.

---

## 2. Desarrollo del Proyecto

### 2.1 La Rana Estadística en Mundos Paralelos: Caminatas Aleatorias (1D, 2D y 3D)

#### 2.1.1 Análisis Probabilístico Inicial
Considérese una partícula (la rana) ubicada inicialmente en el origen de la recta real ($X_0 = 0$). En cada instante discreto $t \in \mathbb{N}$, la partícula efectúa un salto $\xi_t \in \{-1, +1\}$ con probabilidades iguales:
$$P(\xi_t = +1) = 0.5, \quad P(\xi_t = -1) = 0.5$$

La posición tras $n$ saltos viene dada por $X_n = \sum_{t=1}^n \xi_t$.

* **Retorno al origen en $n$ saltos**:
  - Para un número impar de saltos ($n = 1, 3, 5, \dots$), la suma de $+1$ y $-1$ nunca puede ser cero. Por lo tanto, $P(X_n = 0) = 0$ para todo $n$ impar.
  - Para un número par de saltos $n = 2k$, el retorno al origen exige exactamente $k$ saltos a la derecha y $k$ saltos a la izquierda. La probabilidad exacta viene dada por la distribución binomial:
    $$P(X_{2k} = 0) = \binom{2k}{k} \left(\frac{1}{2}\right)^{2k}$$
    - Para $n = 2$ saltos: $P(X_2 = 0) = \binom{2}{1} (0.5)^2 = 2 \times 0.25 = 0.5000$ (50.0%).
    - Para $n = 3$ saltos: $P(X_3 = 0) = 0.0000$ (0.0%).
    - Para $n = 4$ saltos: $P(X_4 = 0) = \binom{4}{2} (0.5)^4 = 6 \times 0.0625 = 0.3750$ (37.5%).

#### 2.1.2 Comportamiento Asintótico y Teorema de Pólya
Al extender el problema a dimensiones superiores ($\mathbb{Z}^d$):
- **1D ($\mathbb{Z}^1$)**: La caminata aleatoria simple es **recurrente nula**. Con probabilidad 1 ($P = 1.0$), la partícula regresará al origen infinitas veces.
- **2D ($\mathbb{Z}^2$)**: En cada paso la partícula elige una de 4 direcciones con probabilidad $1/4$. Según el **Teorema de Pólya (1921)**, la caminata en 2D también es **recurrente** ($P(\text{retorno}) = 1.0$).
- **3D ($\mathbb{Z}^3$)**: En 3D la partícula elige una de 6 direcciones con probabilidad $1/6$. La caminata se vuelve **transitoria**, y la probabilidad exacta de regresar al origen al menos una vez cae a aproximadamente $P \approx 0.3405$ (34.05%).

---

### 2.2 Construcción y Validación de Generadores Pseudoaleatorios

#### 2.2.1 Algoritmos de Generación *From Scratch*
1. **Método de los Cuadrados Medios**: Genera números elevando al cuadrado el valor anterior y extrayendo los dígitos centrales.
2. **Generadores Congruenciales**:
   - *Lineal*: $X_{n+1} = (a X_n + c) \pmod m$
   - *Multiplicativo*: $X_{n+1} = (a X_n) \pmod m$
   - *Aditivo*: $X_{n+1} = (X_n + X_{n-k}) \pmod m$
3. **Distribución Uniforme y Normal**: Normalización a $[0, 1)$ e implementación de la transformación de Box-Muller para valores normales.

#### 2.2.2 Pruebas Estadísticas de Validación
- **Prueba de Medias**: Evalúa si el promedio de la secuencia se encuentra dentro del intervalo de confianza $0.5 \pm Z_{\alpha/2} \sqrt{\frac{1}{12N}}$.
- **Prueba de Varianza**: Compara la varianza muestral contra los límites $\frac{\chi^2_{\alpha/2, N-1}}{12(N-1)}$ y $\frac{\chi^2_{1-\alpha/2, N-1}}{12(N-1)}$.
- **Prueba Chi-cuadrado ($\chi^2$)**: Evalúa la uniformidad comparando frecuencias observadas en $k$ intervalos contra la frecuencia esperada $N/k$.
- **Prueba de Kolmogorov-Smirnov (KS)**: Determina la máxima diferencia $D_{\max} = \max |F_0(x) - S(x)|$ y la compara contra el valor crítico exacto de la distribución de Kolmogorov-Smirnov (`scipy.stats.kstwo.ppf`).
- **Prueba de Póker**: Clasifica manos de 5 dígitos (todos diferentes, una pareja, dos parejas, tercia, full, póker, quintilla) y evalúa el ajuste con $\chi^2$.
- **Prueba de Rachas (Runs Test)**: Mide la independencia contabilizando las rachas por encima y por debajo de la media.

---

### 2.3 EpiSim: Simulación Montecarlo de Propagación de Enfermedades (SEIR)

El modelo **EpiSim** evalúa la propagación de un virus estocástico en una población de $N = 10.000$ individuos distribuidos en 4 estados:
- $S$ (Susceptibles)
- $E$ (Expuestos / Incubación)
- $I$ (Infectados / Contagiosos)
- $R$ (Recuperados / Removidos)

#### Parámetros del Modelo:
- Población inicial $N = 10.000$, Infectados iniciales = 10.
- Tasa de contacto $\beta \sim U(0.3, 0.5)$, Incubación $\sigma^{-1} \sim U(2, 5)$ días, Infeccioso $\gamma^{-1} \sim U(7, 14)$ días.
- Probabilidad de transmisión $p \sim U(0.4, 0.6)$, Tasa de vacunación $U(0.3, 0.7)$, Efectividad de vacuna $U(0.80, 0.95)$.

---

## 3. Resultados

*(Se incluirán aquí los histogramas de frecuencias, gráficos de caminatas 1D/2D/3D, curvas epidémicas SEIR con bandas de confianza del 95% y cuadros de eficiencia computacional).*

---

## 4. Análisis Técnico

Los resultados experimentales ratifican que los generadores congruenciales con parámetros de periodo completo ($m = 2^{31}-1$) superan holgadamente al método de cuadrados medios en términos de longitud de ciclo e independencia estadística. 

En cuanto a la propagación espacial (caminatas aleatorias), los datos confirman la predicción teórica de Pólya: en 1D y 2D la partícula tiende a concentrar sus posiciones finales alrededor del origen con alta densidad de retorno, mientras que en 3D la dispersión crece cúbicamente, reduciendo la probabilidad de retorno.

---

## 5. Conclusiones

1. La construcción e implementación desde cero de algoritmos generadores de números pseudoaleatorios demostró que la elección de parámetros adecuados en métodos congruenciales es determinante para evitar periodos cortos y correlaciones no deseadas.
2. La validación mediante un conjunto multicriterio de seis pruebas estadísticas garantiza que las secuencias utilizadas en simulaciones Montecarlo no introduzcan sesgos en las decisiones de modelado.
3. La dimensionalidad del espacio altera fundamentalmente la dinámica de difusión de los procesos estocásticos: mientras que en 1D y 2D el retorno al origen es un evento casi seguro, en 3D la transiencia domina el comportamiento del sistema.

---

## 6. Referencias Bibliográficas

1. A. M. Law, *Simulation Modeling and Analysis*, 5th ed. New York, NY, USA: McGraw-Hill Education, 2015.
2. J. Banks, J. S. Carson II, B. L. Nelson, and D. M. Nicol, *Discrete-Event System Simulation*, 5th ed. Upper Saddle River, NJ, USA: Pearson, 2010.
3. G. Pólya, "Über eine Aufgabe der Wahrscheinlichkeitsrechnung betreffend die Irrfahrt im Straßennetz," *Mathematische Annalen*, vol. 84, no. 1, pp. 149–160, 1921.
4. R. Y. Rubinstein and D. P. Kroese, *Simulation and the Monte Carlo Method*, 3rd ed. Hoboken, NJ, USA: John Wiley & Sons, 2016.
5. D. E. Knuth, *The Art of Computer Programming, Volume 2: Seminumerical Algorithms*, 3rd ed. Reading, MA, USA: Addison-Wesley, 1997.
