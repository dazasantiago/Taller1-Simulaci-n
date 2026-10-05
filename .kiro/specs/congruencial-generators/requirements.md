# Requirements Document

## Introduction

Este documento especifica los requisitos para la implementación de los generadores de números pseudoaleatorios **Congruencial Lineal** y **Congruencial Multiplicativo** en Python, dentro del proyecto "Taller 1 – Simulación". Ambos generadores forman parte del módulo `src/generadores/congruencial.py` y deben producir secuencias normalizadas en [0, 1) que superen las pruebas estadísticas de uniformidad e independencia ya implementadas en `src/validacion/`.

La restricción de la materia prohíbe usar `random`, `numpy.random` o cualquier librería de generación aleatoria; toda la aritmética es manual.

---

## Glossary

- **Generator**: módulo Python `src/generadores/congruencial.py` que implementa los métodos congruenciales.
- **Congruencial_Lineal**: función `congruencial_lineal(semilla, a, c, m, cantidad)` que implementa el método congruencial lineal (LCG).
- **Congruencial_Multiplicativo**: función `congruencial_multiplicativo(semilla, a, m, cantidad)` que implementa el método congruencial multiplicativo (MCG).
- **Sequence**: lista Python (`list`) de `cantidad` valores `float` en el intervalo [0, 1).
- **Seed / semilla**: valor entero inicial X₀ que arranca la recurrencia.
- **a**: multiplicador entero positivo.
- **c**: incremento entero ≥ 0 (solo en LCG).
- **m**: módulo entero > 1 que define el período máximo posible (2³² para LCG, 2³¹ − 1 para MCG con parámetros por defecto de la app).
- **Statistical_Tests**: conjunto de seis funciones ya implementadas en `src/validacion/` (`means_test`, `variance_test`, `chi_square_test`, `ks_test`, `poker_test`, `runs_test`) que verifican uniformidad e independencia.
- **Catalog**: módulo `app/catalogo.py` que expone los generadores a la interfaz Streamlit mediante `generar_uniforme` / `generar_normal`.

---

## Requirements

### Requisito 1: Generación de secuencia congruencial lineal

**User Story:** Como estudiante de simulación, quiero invocar `congruencial_lineal(semilla, a, c, m, cantidad)` para obtener una secuencia pseudoaleatoria uniforme, de modo que pueda usarla como entrada en las pruebas estadísticas y en la interfaz gráfica.

#### Criterios de aceptación

1. THE `Congruencial_Lineal` SHALL aceptar exactamente los parámetros enteros `semilla`, `a`, `c`, `m` y el entero `cantidad`.
2. THE `Congruencial_Lineal` SHALL calcular cada término siguiente con la recurrencia X_{n+1} = (a × X_n + c) mod m.
3. THE `Congruencial_Lineal` SHALL normalizar cada X_i dividiendo entre m antes de agregarlo a la `Sequence`, produciendo valores `float` en [0, 1).
4. THE `Congruencial_Lineal` SHALL retornar una `Sequence` de exactamente `cantidad` valores.
5. IF `cantidad` ≤ 0, THEN THE `Congruencial_Lineal` SHALL retornar una lista vacía.
6. IF `m` ≤ 1, THEN THE `Congruencial_Lineal` SHALL lanzar un `ValueError` con un mensaje que indique que m debe ser mayor que 1.
7. IF `a` < 1 OR `a` ≥ `m`, THEN THE `Congruencial_Lineal` SHALL lanzar un `ValueError` con un mensaje que indique que a debe estar en el rango [1, m-1].
8. IF `c` < 0 OR `c` ≥ `m`, THEN THE `Congruencial_Lineal` SHALL lanzar un `ValueError` con un mensaje que indique que c debe estar en el rango [0, m-1].
9. IF `semilla` < 0 OR `semilla` ≥ `m`, THEN THE `Congruencial_Lineal` SHALL lanzar un `ValueError` con un mensaje que indique que la semilla debe estar en el rango [0, m-1].
10. WHERE los parámetros son `a = 1 664 525`, `c = 1 013 904 223`, `m = 2³²` y `semilla` en [0, m-1], THE `Congruencial_Lineal` SHALL producir una `Sequence` de 1 000 valores que pase `means_test` de `Statistical_Tests`.
11. WHERE los parámetros son `a = 1 664 525`, `c = 1 013 904 223`, `m = 2³²` y `semilla` en [0, m-1], THE `Congruencial_Lineal` SHALL producir una `Sequence` de 1 000 valores que pase `variance_test` de `Statistical_Tests`.
12. WHERE los parámetros son `a = 1 664 525`, `c = 1 013 904 223`, `m = 2³²` y `semilla` en [0, m-1], THE `Congruencial_Lineal` SHALL producir una `Sequence` de 100 valores en la que todos los elementos son distintos entre sí.

---

### Requisito 2: Generación de secuencia congruencial multiplicativa

**User Story:** Como estudiante de simulación, quiero invocar `congruencial_multiplicativo(semilla, a, m, cantidad)` para obtener una secuencia pseudoaleatoria uniforme sin incremento, de modo que pueda comparar su calidad estadística con el método lineal.

#### Criterios de aceptación

1. THE `Congruencial_Multiplicativo` SHALL aceptar exactamente los parámetros enteros `semilla` (> 0), `a` (≥ 1), `m` (≥ 2) y el entero `cantidad`.
2. THE `Congruencial_Multiplicativo` SHALL calcular cada término siguiente con la recurrencia X_{n+1} = (a × X_n) mod m, sin ningún incremento.
3. THE `Congruencial_Multiplicativo` SHALL normalizar cada X_i dividiendo entre m antes de agregarlo a la `Sequence`, produciendo valores `float` en [0, 1).
4. THE `Congruencial_Multiplicativo` SHALL retornar una `list` de exactamente `cantidad` valores `float`.
5. IF `cantidad` ≤ 0, THEN THE `Congruencial_Multiplicativo` SHALL retornar una lista vacía.
6. IF `m` ≤ 1, THEN THE `Congruencial_Multiplicativo` SHALL lanzar un `ValueError` con mensaje descriptivo.
7. IF `a` < 1, THEN THE `Congruencial_Multiplicativo` SHALL lanzar un `ValueError` con mensaje descriptivo.
8. IF `semilla` ≤ 0, THEN THE `Congruencial_Multiplicativo` SHALL lanzar un `ValueError` indicando que la semilla debe ser un entero positivo.
9. IF `semilla` mod `m` == 0, THEN THE `Congruencial_Multiplicativo` SHALL lanzar un `ValueError` indicando que la semilla no puede ser múltiplo de m (produciría secuencia degenerada de ceros).
10. WHERE los parámetros son `a = 16 807`, `m = 2³¹ − 1`, `semilla` en [1, m-1] no múltiplo de m, THE `Congruencial_Multiplicativo` SHALL producir una `Sequence` de 1 000 valores que pase `means_test` de `Statistical_Tests` con nivel de significancia α = 0.05.
11. WHERE los parámetros son `a = 16 807`, `m = 2³¹ − 1`, `semilla` en [1, m-1] no múltiplo de m, THE `Congruencial_Multiplicativo` SHALL producir una `Sequence` de 1 000 valores que pase `variance_test` de `Statistical_Tests` con nivel de significancia α = 0.05.

---

### Requisito 3: Compatibilidad con el catálogo de la interfaz

**User Story:** Como usuario de la interfaz Streamlit, quiero que ambos generadores aparezcan automáticamente en el selector de la pestaña "Generación", de modo que pueda configurar parámetros y visualizar histogramas sin necesidad de tocar el código.

#### Criterios de aceptación

1. THE `Generator` SHALL exportar `congruencial_lineal` y `congruencial_multiplicativo` como nombres que se resuelven a un callable mediante `getattr` sobre el módulo importado con `importlib.import_module("src.generadores.congruencial")`.
2. WHEN `Catalog` invoca `generar_uniforme("congruencial_lineal", parametros, cantidad)`, THE `Generator` SHALL retornar una `list` de exactamente `cantidad` valores `float` en [0.0, 1.0) sin lanzar excepciones, siempre que `parametros` contenga `semilla` en [0, m-1], `a` en [1, m-1], `c` en [0, m-1] y `m` > 1.
3. WHEN `Catalog` invoca `generar_uniforme("congruencial_multiplicativo", parametros, cantidad)`, THE `Generator` SHALL retornar una `list` de exactamente `cantidad` valores `float` en [0.0, 1.0) sin lanzar excepciones, siempre que `parametros` contenga `semilla` en [1, m-1] no múltiplo de m, `a` ≥ 1 y `m` ≥ 2.
4. THE `Catalog` SHALL implementar la función `generar_uniforme` en `distribuciones.py`, dado que `bases_disponibles()` definida en `catalogo.py` depende de su existencia para resolver los generadores registrados.

---

### Requisito 4: Restricción de librería

**User Story:** Como evaluador del taller, quiero que los generadores no usen ninguna librería de generación aleatoria, de modo que la implementación demuestre comprensión de los algoritmos.

#### Criterios de aceptación

1. THE `Generator` SHALL implementar `congruencial_lineal` y `congruencial_multiplicativo` sin importar ni llamar a `random`, `numpy.random`, `secrets`, ni ningún módulo cuya función principal sea la generación de números aleatorios.
2. THE `Generator` SHALL calcular cada valor de la secuencia mediante los operadores aritméticos estándar de Python (`*`, `+`, `%`) sobre operandos de tipo `int`, sin convertir los operandos a `float` durante la recurrencia.

---

### Requisito 5: Propiedades de corrección (round-trip e invariantes)

**User Story:** Como desarrollador, quiero contar con propiedades formalmente verificables sobre la salida de los generadores, de modo que las pruebas de propiedad detecten regresiones automáticamente.

#### Criterios de aceptación

1. THE `Congruencial_Lineal` SHALL producir una `list` de exactamente `n` elementos, todos `float` en [0.0, 1.0), para cualquier invocación con parámetros válidos `semilla` en [0, m-1], `a` en [1, m-1], `c` en [0, m-1], `m` > 1 y `n` ≥ 1.
2. THE `Congruencial_Multiplicativo` SHALL producir una `list` de exactamente `n` elementos, todos `float` en [0.0, 1.0), para cualquier invocación con parámetros válidos `semilla` en [1, m-1] no múltiplo de m, `a` ≥ 1, `m` ≥ 2 y `n` ≥ 1.
3. WHEN `congruencial_lineal` se invoca dos veces con los mismos parámetros (`semilla`, `a`, `c`, `m`, `n`), THE `Generator` SHALL producir secuencias idénticas (determinismo respecto a la semilla).
4. WHEN `congruencial_multiplicativo` se invoca dos veces con los mismos parámetros (`semilla`, `a`, `m`, `n`), THE `Generator` SHALL producir secuencias idénticas (determinismo respecto a la semilla).
5. IF `congruencial_lineal` se invoca con cualquier combinación de parámetros inválidos (`m` ≤ 1, `a` < 1, `a` ≥ `m`, `c` < 0, `c` ≥ `m`, `semilla` < 0, o `semilla` ≥ `m`), THEN THE `Congruencial_Lineal` SHALL lanzar un `ValueError`.
6. IF `congruencial_multiplicativo` se invoca con cualquier combinación de parámetros inválidos (`m` ≤ 1, `a` < 1, `semilla` ≤ 0, o `semilla` múltiplo de `m`), THEN THE `Congruencial_Multiplicativo` SHALL lanzar un `ValueError`.
