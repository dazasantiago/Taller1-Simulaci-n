# Punto 3 — Generadores y Validación de Números Pseudoaleatorios

Módulo en Python que implementa generadores de números pseudoaleatorios
desde cero y los somete a pruebas estadísticas de validación.
No se usa `random`, `numpy.random` ni ninguna librería de generación aleatoria.

## Cuadro técnico

| Componente | Detalle |
|------------|---------|
| Lenguaje | Python 3.14.3 |
| Sistema operativo | Windows 11 Home |
| Procesador | AMD Ryzen 7 7435HS |
| Memoria RAM | 16 GB |

## Cómo ejecutarlo

Instalar dependencias:
```bash
pip install -r requirements.txt
```

Correr la interfaz gráfica:
```bash
streamlit run app/main.py
```

Abrir `http://localhost:8501` en el navegador.

## Semillas de ejemplo

En `data/seeds/` hay dos archivos listos para cargar desde la UI
(pestaña Generación → "Importar semillas"):

| Archivo | Formato |
|---------|---------|
| `semillas_ejemplo.txt` | un valor por línea |
| `semillas_ejemplo.csv` | columna `semilla` |

## Generadores implementados

### Cuadrados Medios — `cuadrados_medios`

Eleva la semilla al cuadrado, toma los `n_digitos` dígitos centrales como siguiente valor
y repite. El resultado son enteros en `[0, 10^n_digitos)`.

| Parámetro | Tipo | Descripción | Restricción |
|-----------|------|-------------|-------------|
| `semilla` | `int` | Valor inicial | `[0, 10^n_digitos - 1]` |
| `n_digitos` | `int` | Dígitos del método | `>= 3` |
| `cantidad` | `int` | Cantidad de valores | `>= 0` |

Retorna `list[int]`. Lanza `TypeError` si algún argumento no es entero, `ValueError` si está fuera de rango.

> La semilla debe tener exactamente `n_digitos` dígitos. Con `n_digitos=4` usar semillas
> como `1234`, `5765`, `9731`. Evitar semillas simétricas (`1001`, `1111`) — tienden a
> ciclos cortos o degeneran en cero.

```python
from src.generadores.cuadrados_medios import cuadrados_medios

enteros = cuadrados_medios(semilla=1234, n_digitos=4, cantidad=1000)
uniformes = [x / 10**4 for x in enteros]  # R_i en [0.0, 1.0)
```

### Congruencial Lineal — `linear_congruential`

Recurrencia: `X_{n+1} = (a * X_n + c) mod m`

| Parámetro | Tipo | Descripción | Restricción |
|-----------|------|-------------|-------------|
| `seed` | `int` | Valor inicial X_0 | `[0, m-1]` |
| `a` | `int` | Multiplicador | `[1, m-1]` |
| `c` | `int` | Incremento | `[0, m-1]` |
| `m` | `int` | Módulo | `> 1` |
| `count` | `int` | Cantidad de valores | retorna `[]` si `<= 0` |

Retorna `list[int]` en `[0, m)`. Lanza `ValueError` si algún parámetro está fuera de rango.

Parámetros de referencia — ANSI C (ISO/IEC 9899:1990):
`a = 1103515245`, `c = 12345`, `m = 2147483648 (2³¹)` — período completo garantizado por el Teorema de Dobell.

```python
from src.generadores.congruencial import linear_congruential

enteros = linear_congruential(seed=12345, a=1103515245, c=12345, m=2147483648, count=1000)
uniformes = [x / 2147483648 for x in enteros]  # R_i en [0.0, 1.0)
```

### Congruencial Multiplicativo — `multiplicative_congruential`

Recurrencia: `X_{n+1} = (a * X_n) mod m` — caso especial con `c = 0`.

| Parámetro | Tipo | Descripción | Restricción |
|-----------|------|-------------|-------------|
| `seed` | `int` | Valor inicial X_0 | `> 0`, no múltiplo de `m` |
| `a` | `int` | Multiplicador | `>= 1` |
| `m` | `int` | Módulo | `> 1` |
| `count` | `int` | Cantidad de valores | retorna `[]` si `<= 0` |

Retorna `list[int]` en `[0, m)`. Lanza `ValueError` si algún parámetro está fuera de rango.

Parámetros de referencia — L'Ecuyer (1988), CACM:
`a = 48271`, `m = 2147483647 (2³¹−1, primo de Mersenne)` — período máximo `m−1`.

```python
from src.generadores.congruencial import multiplicative_congruential

enteros = multiplicative_congruential(seed=12345, a=48271, m=2147483647, count=1000)
uniformes = [x / 2147483647 for x in enteros]  # R_i en [0.0, 1.0)
```

### Normalización y distribución Normal

Los generadores producen enteros `X_i`. La conversión a uniformes `R_i ∈ [0, 1)`
y a normales `N_i ~ N(0,1)` (Box-Muller) se hace en `src/generadores/distribuciones.py`.
La UI lo hace automáticamente al seleccionar el método.

## Pruebas estadísticas disponibles

| Prueba | Función |
|--------|---------|
| Medias | `prueba_medias` |
| Varianza | `prueba_varianza` |
| Chi-cuadrado | `chi_square_test` |
| Kolmogorov-Smirnov | `prueba_ks` |
| Póker | `poker_test` |
| Rachas | `runs_test` |

Todas reciben `list[float]` con valores en `[0, 1)` y retornan el estadístico,
valor crítico y si la secuencia pasa la prueba.

## Estructura

```
punto 3 - generadores/
├── app/main.py                    # Interfaz Streamlit
├── src/
│   ├── generadores/
│   │   ├── congruencial.py        # LCG y MCG
│   │   ├── cuadrados_medios.py    # Cuadrados Medios
│   │   └── distribuciones.py      # Uniforme y Normal
│   └── validacion/                # 6 pruebas estadísticas
├── data/seeds/                    # Semillas de ejemplo
└── requirements.txt
```

## Errores posibles

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: m debe ser mayor que 1` | Módulo `m <= 1` | Usar `m >= 2` |
| `ValueError: a debe estar en [1, m-1]` | Multiplicador fuera de rango | Ajustar `a` dentro del rango |
| `ValueError: seed debe estar en [0, m-1]` | Semilla fuera de rango para LCG | Usar semilla entre 0 y `m-1` |
| `ValueError: seed debe ser un entero positivo` | Semilla `<= 0` en MCG | Usar semilla `>= 1` |
| `ValueError: seed no puede ser múltiplo de m` | Semilla degenerada en MCG | Cambiar semilla |
| `ValueError: El número de dígitos debe ser >= 3` | `n_digitos < 3` en Cuadrados Medios | Usar `n_digitos >= 3` |
| `ValueError: La semilla debe estar entre 0 y ...` | Semilla fuera de rango en Cuadrados Medios | Usar semilla de exactamente `n_digitos` dígitos |
| `TypeError` en Cuadrados Medios | Argumento no entero | Verificar tipos de entrada |
| Histograma no uniforme | Parámetros que no cumplen condiciones de período máximo | Usar los parámetros de referencia |
| Secuencia degenera en cero | Semilla múltiplo de `m` (MCG) o semilla `0` en Cuadrados Medios | Cambiar semilla |

## Nota sobre el uso de herramientas de inteligencia artificial

Claude (Anthropic) ayudó a reescribir las pruebas de validación de Chi-cuadrado,
Póker y Rachas (`src/validacion/prueba_chi_cuadrado.py`, `prueba_poker.py`,
`prueba_rachas.py`) en una versión más lineal y sin dependencias avanzadas de
Python, bajo dirección del estudiante en cada decisión de diseño.
