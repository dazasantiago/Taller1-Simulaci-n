# Design Document — `congruencial-generators`

## Overview

Este documento describe el diseño técnico de los módulos
`src/generadores/congruencial.py` y `src/generadores/distribuciones.py`
dentro del proyecto "Taller 1 – Simulación, punto 3 – generadores".

El objetivo es implementar dos generadores de números pseudoaleatorios
clásicos (Congruencial Lineal y Congruencial Multiplicativo) junto con
la capa de despacho `generar_uniforme` que los expone a la interfaz
Streamlit a través de `app/catalogo.py`. Toda la aritmética es
Python puro; no se permite ninguna importación de librerías de
generación aleatoria.

### Contexto en el sistema

```
app/catalogo.py
    └─ generar_uniforme / generar_normal   (distribuciones.py)
            └─ congruencial_lineal / congruencial_multiplicativo
                                           (congruencial.py)
```

`catalogo.py` es el único punto de entrada de la capa `app/` hacia
`src/`. Carga los módulos en tiempo de ejecución mediante
`importlib.import_module` y revela un método en la UI solo si la
función correspondiente puede resolverse por nombre.

---

## Architecture

La arquitectura es de capas planas con dependencia estrictamente
unidireccional:

```
┌─────────────────────────────────────────────────┐
│               app/  (Streamlit)                 │
│  catalogo.py · estado.py · tab_generacion.py …  │
└──────────────────┬──────────────────────────────┘
                   │  importlib (en tiempo de ejecución)
┌──────────────────▼──────────────────────────────┐
│            src/generadores/                     │
│  distribuciones.py  ──►  congruencial.py        │
│                     ──►  cuadrados_medios.py    │
└─────────────────────────────────────────────────┘
```

- `congruencial.py` no importa nada; es aritmética pura.
- `distribuciones.py` importa las funciones de los generadores base
  usando `importlib` o importación directa (sin librerías aleatorias).
- El catálogo descubre los generadores disponibles en tiempo de
  ejecución; si una función no existe, simplemente no aparece en la UI.

### Decisiones de diseño

| Decisión | Alternativas consideradas | Justificación |
|---|---|---|
| Generadores base devuelven `list[int]` (sin normalizar) | Devolver `list[float]` directamente | El contrato de `docs/README.md` separa la generación entera de la normalización. `generar_uniforme` centraliza la normalización, lo que permite reutilizar los enteros en otros contextos. |
| `generar_uniforme` normaliza con `x / m` | Normalizar dentro del generador | Un único lugar de normalización evita errores de off-by-one y facilita el testing independiente. |
| Validaciones de parámetros al inicio de la función | Validar en `generar_uniforme` | Las restricciones son propias de cada algoritmo; centralizarlas en el generador hace el módulo autónomo. |
| `ValueError` con mensajes descriptivos | Aserciones / retornar None | `ValueError` es el idioma estándar de Python para parámetros inválidos; permite que la app lo capture y muestre al usuario. |

---

## Components and Interfaces

### `src/generadores/congruencial.py`

Este módulo no tiene imports. Expone tres funciones públicas (las dos
requeridas más `congruencial_aditivo` que ya está registrada en el
catálogo):

```python
def congruencial_lineal(
    semilla: int,
    a: int,
    c: int,
    m: int,
    cantidad: int,
) -> list[int]:
    """
    Genera `cantidad` enteros X_i en [0, m) mediante la recurrencia:
        X_{n+1} = (a * X_n + c) % m

    Retorna lista vacía si cantidad <= 0.

    Raises:
        ValueError: si m <= 1, a no está en [1, m-1],
                    c no está en [0, m-1], o semilla no está en [0, m-1].
    """

def congruencial_multiplicativo(
    semilla: int,
    a: int,
    m: int,
    cantidad: int,
) -> list[int]:
    """
    Genera `cantidad` enteros X_i en [0, m) mediante la recurrencia:
        X_{n+1} = (a * X_n) % m

    Retorna lista vacía si cantidad <= 0.

    Raises:
        ValueError: si m <= 1, a < 1, semilla <= 0,
                    o semilla % m == 0 (secuencia degenerada).
    """
```

> **Nota de contrato:** el `docs/README.md` del proyecto especifica que
> los generadores base devuelven `list[int]` (valores sin normalizar en
> `[0, m)`), mientras que el `requirements.md` describe la salida como
> `list[float]` en `[0, 1)`. La fuente de verdad arquitectónica es
> `docs/README.md`: los generadores base devuelven enteros y
> `generar_uniforme` en `distribuciones.py` realiza la normalización.
> Esta separación facilita el testing independiente de la recurrencia.

### `src/generadores/distribuciones.py`

```python
def generar_uniforme(
    metodo: str,
    parametros: dict,
    cantidad: int,
) -> list[float]:
    """
    Despacha la generación de `cantidad` valores uniformes en [0, 1).

    `metodo`: nombre de la función generadora base
              ("congruencial_lineal", "congruencial_multiplicativo", …).
    `parametros`: dict con todos los argumentos del generador base
                  excepto `cantidad`, por ejemplo:
                  {"semilla": 42, "a": 1664525, "c": 1013904223, "m": 4294967296}

    Normaliza: r_i = X_i / m   donde m = parametros["m"].

    No usa ninguna librería de aleatoriedad.
    """

def generar_normal(
    metodo_base: str,
    parametros: dict,
    cantidad: int,
) -> list[float]:
    """
    Genera `cantidad` valores ~N(0, 1) aplicando la transformada Box-Muller
    sobre pares de uniformes producidos por `generar_uniforme`.
    """
```

### Cómo los invoca `app/catalogo.py`

```python
# catalogo.py (ya implementado, no se modifica)
funcion = getattr(
    importlib.import_module("src.generadores.distribuciones"),
    "generar_uniforme",
)
valores = funcion("congruencial_lineal", parametros, cantidad)
# parametros = {"semilla": X0, "a": 1664525, "c": 1013904223, "m": 4294967296}
```

`distribuciones.py` extrae `m` de `parametros` para normalizar y pasa
el resto al generador base como `**kwargs` (omitiendo `m` solo si el
generador no lo necesita, aunque en LCG y MCG ambos lo necesitan).

---

## Data Models

No hay estructuras de datos persistentes. Los únicos tipos de datos son:

| Nombre | Tipo Python | Descripción |
|---|---|---|
| Secuencia entera | `list[int]` | Salida cruda de los generadores base. Valores en `[0, m)`. |
| Secuencia uniforme | `list[float]` | Salida de `generar_uniforme`. Valores en `[0.0, 1.0)`. |
| `parametros` dict | `dict[str, int]` | Argumentos del generador base. Llaves: `"semilla"`, `"a"`, `"c"` (solo LCG), `"m"`. |

### Parámetros de referencia del catálogo

| Generador | `a` | `c` | `m` | Período |
|---|---|---|---|---|
| LCG (congruencial_lineal) | 1 664 525 | 1 013 904 223 | 2³² = 4 294 967 296 | 2³² (completo) |
| MCG (congruencial_multiplicativo) | 16 807 | — | 2³¹ − 1 = 2 147 483 647 | 2³¹ − 2 (máximo) |

Los parámetros LCG son los de Numerical Recipes (Knuth); los MCG son
los del generador de Park-Miller (MINSTD). Ambos están pre-cargados en
`app/catalogo.py` como valores por defecto — no es necesario hard-codearlos en los generadores.

---

## Correctness Properties

*Una propiedad es una característica o comportamiento que debe cumplirse
en todas las ejecuciones válidas del sistema — esencialmente, un
enunciado formal sobre lo que el sistema debe hacer. Las propiedades
sirven como puente entre especificaciones legibles por humanos y
garantías de corrección verificables por máquina.*

---

### Property 1: Invariantes de salida del LCG

*Para cualquier* invocación válida de `congruencial_lineal` con
`semilla ∈ [0, m-1]`, `a ∈ [1, m-1]`, `c ∈ [0, m-1]`, `m > 1` y
`n ≥ 1`, la función debe retornar exactamente `n` enteros, todos en
el intervalo `[0, m)`.

**Validates: Requirements 1.3, 1.4, 5.1**

---

### Property 2: Corrección de la recurrencia LCG

*Para cualquier* invocación válida de `congruencial_lineal` con `n ≥ 2`,
cada par de elementos consecutivos `(X[i], X[i+1])` de la secuencia
entera debe satisfacer `X[i+1] == (a * X[i] + c) % m`.

**Validates: Requirements 1.2**

---

### Property 3: Determinismo del LCG

*Para cualquier* conjunto de parámetros válidos
`(semilla, a, c, m, n)`, invocar `congruencial_lineal` dos veces debe
producir secuencias idénticas.

**Validates: Requirements 5.3**

---

### Property 4: LCG rechaza parámetros inválidos

*Para cualquier* invocación de `congruencial_lineal` con al menos un
parámetro inválido (`m ≤ 1`, `a < 1`, `a ≥ m`, `c < 0`, `c ≥ m`,
`semilla < 0`, o `semilla ≥ m`), la función debe lanzar `ValueError`.

**Validates: Requirements 1.6, 1.7, 1.8, 1.9, 5.5**

---

### Property 5: Unicidad con parámetros de referencia LCG

*Para cualquier* semilla en `[0, 2³²-1]` con los parámetros de
referencia `a=1664525`, `c=1013904223`, `m=2³²`, los primeros 100
valores de la secuencia deben ser todos distintos entre sí
(período mucho mayor que 100 garantiza que no haya repeticiones en ese
prefijo).

**Validates: Requirements 1.12**

---

### Property 6: Invariantes de salida del MCG

*Para cualquier* invocación válida de `congruencial_multiplicativo` con
`semilla ∈ [1, m-1]` no múltiplo de `m`, `a ≥ 1`, `m ≥ 2` y `n ≥ 1`,
la función debe retornar exactamente `n` enteros, todos en `[0, m)`.

**Validates: Requirements 2.3, 2.4, 5.2**

---

### Property 7: Corrección de la recurrencia MCG

*Para cualquier* invocación válida de `congruencial_multiplicativo` con
`n ≥ 2`, cada par de elementos consecutivos `(X[i], X[i+1])` debe
satisfacer `X[i+1] == (a * X[i]) % m`.

**Validates: Requirements 2.2**

---

### Property 8: Determinismo del MCG

*Para cualquier* conjunto de parámetros válidos `(semilla, a, m, n)`,
invocar `congruencial_multiplicativo` dos veces debe producir secuencias
idénticas.

**Validates: Requirements 5.4**

---

### Property 9: MCG rechaza parámetros inválidos

*Para cualquier* invocación de `congruencial_multiplicativo` con al
menos un parámetro inválido (`m ≤ 1`, `a < 1`, `semilla ≤ 0`, o
`semilla % m == 0`), la función debe lanzar `ValueError`.

**Validates: Requirements 2.5, 2.6, 2.7, 2.8, 2.9, 5.6**

---

### Property 10: generar_uniforme produce floats en [0, 1)

*Para cualquier* parámetro válido pasado a `generar_uniforme` con
`metodo ∈ {"congruencial_lineal", "congruencial_multiplicativo"}` y
`n ≥ 1`, todos los valores del resultado deben ser `float` en
`[0.0, 1.0)`.

**Validates: Requirements 3.2, 3.3**

---

## Error Handling

### Validaciones en `congruencial_lineal`

```python
if m <= 1:
    raise ValueError(f"m debe ser mayor que 1 (recibido: m={m})")
if not (1 <= a <= m - 1):
    raise ValueError(f"a debe estar en [1, m-1] (recibido: a={a}, m={m})")
if not (0 <= c <= m - 1):
    raise ValueError(f"c debe estar en [0, m-1] (recibido: c={c}, m={m})")
if not (0 <= semilla <= m - 1):
    raise ValueError(
        f"semilla debe estar en [0, m-1] (recibido: semilla={semilla}, m={m})"
    )
```

### Validaciones en `congruencial_multiplicativo`

```python
if m <= 1:
    raise ValueError(f"m debe ser mayor que 1 (recibido: m={m})")
if a < 1:
    raise ValueError(f"a debe ser al menos 1 (recibido: a={a})")
if semilla <= 0:
    raise ValueError(
        f"semilla debe ser un entero positivo (recibido: semilla={semilla})"
    )
if semilla % m == 0:
    raise ValueError(
        f"semilla no puede ser múltiplo de m "
        f"(semilla={semilla}, m={m}): produciría secuencia degenerada de ceros"
    )
```

### Manejo en `generar_uniforme`

`generar_uniforme` no captura las excepciones de los generadores base;
las propaga directamente. `app/catalogo.py` (función `ejecutar_prueba`)
y `app/tab_generacion.py` ya tienen los bloques `try/except` necesarios
para mostrar el error al usuario en la interfaz.

---

## Testing Strategy

### Herramienta de property-based testing

Se usa **Hypothesis** (la librería estándar de PBT para Python).

```
pip install hypothesis
```

La suite de tests vive en `tests/` (ya existe `tests/test_placeholder.py`
con la infraestructura de pytest).

### Configuración de Hypothesis

Cada test de propiedad se decora con `@settings(max_examples=100)` como
mínimo. Para propiedades críticas (corrección de recurrencia) se puede
usar `max_examples=200`.

El tag de referencia al diseño se incluye como comentario en cada test:
```python
# Feature: congruencial-generators, Property N: <texto de la propiedad>
```

### Estrategias de generación (`st`)

```python
from hypothesis import given, settings, strategies as st

# Módulo válido: m > 1, 1 <= a <= m-1, 0 <= c <= m-1, 0 <= semilla <= m-1
m_strategy    = st.integers(min_value=2, max_value=2**16)
a_lcg_strat   = st.integers(min_value=1).flatmap(lambda m: st.integers(1, m-1))
# etc. — se detalla en la implementación de los tests
```

### Plan de tests

#### Tests de propiedad (Hypothesis)

| Test | Propiedad | `max_examples` |
|---|---|---|
| `test_lcg_output_invariants` | Property 1 | 100 |
| `test_lcg_recurrence` | Property 2 | 200 |
| `test_lcg_determinism` | Property 3 | 100 |
| `test_lcg_rejects_invalid` | Property 4 | 100 |
| `test_lcg_uniqueness_reference_params` | Property 5 | 100 |
| `test_mcg_output_invariants` | Property 6 | 100 |
| `test_mcg_recurrence` | Property 7 | 200 |
| `test_mcg_determinism` | Property 8 | 100 |
| `test_mcg_rejects_invalid` | Property 9 | 100 |
| `test_generar_uniforme_range` | Property 10 | 100 |

#### Tests de ejemplo (pytest)

| Test | Criterio cubierto |
|---|---|
| `test_lcg_empty_on_zero_cantidad` | Req 1.5 |
| `test_mcg_empty_on_zero_cantidad` | Req 2.5 |
| `test_lcg_passes_means_test` | Req 1.10 (2 semillas de referencia) |
| `test_lcg_passes_variance_test` | Req 1.11 (2 semillas de referencia) |
| `test_mcg_passes_means_test` | Req 2.10 |
| `test_mcg_passes_variance_test` | Req 2.11 |
| `test_module_no_random_imports` | Req 4.1 (inspección AST) |
| `test_generar_uniforme_callable` | Req 3.4 |

### Ejecución

```bash
# desde punto 3 - generadores/
pytest tests/ --tb=short -q
```

> Los tests de propiedad con Hypothesis se ejecutan en modo determinista
> por defecto (Hypothesis reutiliza la base de datos de ejemplos
> fallidos previos). Para correr con semilla fija: `--hypothesis-seed=0`.
