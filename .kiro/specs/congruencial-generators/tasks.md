# Implementation Plan: congruencial-generators

## Overview

Implementación incremental de los generadores Congruencial Lineal (LCG) y Congruencial Multiplicativo (MCG) en `src/generadores/congruencial.py`, seguida de la capa de despacho `generar_uniforme` en `src/generadores/distribuciones.py`. Cada paso construye sobre el anterior y termina con la integración completa en el catálogo Streamlit. Los tests de propiedad con Hypothesis validan corrección en cada nivel.

## Tasks

- [x] 1. Agregar `hypothesis` a las dependencias del proyecto
  - Añadir `hypothesis==6.112.0` a `requirements.txt` (después de `pytest`).
  - _Requirements: (infraestructura de tests — prerequisito para todas las sub-tareas de propiedad)_

- [x] 2. Implementar `congruencial_lineal` en `src/generadores/congruencial.py`
  - [x] 2.1 Escribir la función `congruencial_lineal(semilla, a, c, m, cantidad) -> list[int]`
    - Validar parámetros en el orden: `m <= 1`, `a` fuera de `[1, m-1]`, `c` fuera de `[0, m-1]`, `semilla` fuera de `[0, m-1]`; lanzar `ValueError` con mensaje descriptivo en cada caso.
    - Si `cantidad <= 0`, retornar lista vacía inmediatamente.
    - Calcular la recurrencia `X_{n+1} = (a * X_n + c) % m` con aritmética entera pura (sin `float` durante el cálculo).
    - Acumular los `cantidad` valores en una lista y retornarla.
    - No importar ningún módulo en este archivo.
    - _Requirements: 1.1, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 4.1, 4.2_

  - [ ]* 2.2 Escribir tests de propiedad para `congruencial_lineal` (Properties 1–5)
    - Añadir `tests/test_congruencial_lineal.py`.
    - Definir estrategias Hypothesis: `m_st = st.integers(min_value=2, max_value=2**16)`, `a_st` dependiente de `m`, `c_st` dependiente de `m`, `semilla_st` dependiente de `m`.
    - **Property 1: Invariantes de salida del LCG** — para parámetros válidos y `n ≥ 1`, la lista tiene exactamente `n` enteros todos en `[0, m)`. `@settings(max_examples=100)`. **Validates: Requirements 1.3, 1.4, 5.1**
    - **Property 2: Corrección de la recurrencia LCG** — para `n ≥ 2`, cada par `(X[i], X[i+1])` satisface `X[i+1] == (a * X[i] + c) % m`. `@settings(max_examples=200)`. **Validates: Requirements 1.2**
    - **Property 3: Determinismo del LCG** — dos invocaciones con los mismos parámetros producen listas idénticas. `@settings(max_examples=100)`. **Validates: Requirements 5.3**
    - **Property 4: LCG rechaza parámetros inválidos** — cualquier combinación de parámetros inválidos lanza `ValueError`. `@settings(max_examples=100)`. **Validates: Requirements 1.6, 1.7, 1.8, 1.9, 5.5**
    - **Property 5: Unicidad con parámetros de referencia LCG** — para `a=1664525`, `c=1013904223`, `m=2**32`, los primeros 100 valores son todos distintos. `@settings(max_examples=100)`. **Validates: Requirements 1.12**
    - Incluir el comentario `# Feature: congruencial-generators, Property N: <texto>` en cada test.
    - _Requirements: 1.2, 1.3, 1.4, 1.6, 1.7, 1.8, 1.9, 1.12, 5.1, 5.3, 5.5_

  - [ ]* 2.3 Escribir tests de ejemplo para `congruencial_lineal`
    - En `tests/test_congruencial_lineal.py`, agregar:
      - `test_lcg_empty_on_zero_cantidad`: verifica que `cantidad=0` retorna `[]`. _Requirements: 1.5_
      - `test_lcg_empty_on_negative_cantidad`: verifica que `cantidad=-1` retorna `[]`. _Requirements: 1.5_
      - `test_lcg_passes_means_test`: llama `means_test` sobre 1000 valores con parámetros de referencia y verifica `pasa_prueba == True`. _Requirements: 1.10_
      - `test_lcg_passes_variance_test`: ídem con `prueba_varianza`. _Requirements: 1.11_
      - `test_module_no_random_imports`: inspecciona el AST de `congruencial.py` y verifica que no importa `random`, `numpy.random` ni `secrets`. _Requirements: 4.1_

- [x] 3. Checkpoint — verificar LCG
  - Ejecutar `pytest tests/test_congruencial_lineal.py --tb=short -q` desde `punto 3 - generadores/`.
  - Asegurarse de que todos los tests pasen; resolver cualquier fallo antes de continuar.

- [x] 4. Implementar `congruencial_multiplicativo` en `src/generadores/congruencial.py`
  - [x] 4.1 Escribir la función `congruencial_multiplicativo(semilla, a, m, cantidad) -> list[int]`
    - Validar en orden: `m <= 1`, `a < 1`, `semilla <= 0`, `semilla % m == 0`; lanzar `ValueError` con mensaje descriptivo en cada caso.
    - Si `cantidad <= 0`, retornar lista vacía.
    - Calcular la recurrencia `X_{n+1} = (a * X_n) % m` sin incremento, con aritmética entera pura.
    - Acumular `cantidad` valores y retornar la lista.
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 4.1, 4.2_

  - [ ]* 4.2 Escribir tests de propiedad para `congruencial_multiplicativo` (Properties 6–9)
    - Añadir `tests/test_congruencial_multiplicativo.py`.
    - **Property 6: Invariantes de salida del MCG** — para parámetros válidos y `n ≥ 1`, la lista tiene exactamente `n` enteros en `[0, m)`. `@settings(max_examples=100)`. **Validates: Requirements 2.3, 2.4, 5.2**
    - **Property 7: Corrección de la recurrencia MCG** — para `n ≥ 2`, cada par `(X[i], X[i+1])` satisface `X[i+1] == (a * X[i]) % m`. `@settings(max_examples=200)`. **Validates: Requirements 2.2**
    - **Property 8: Determinismo del MCG** — dos invocaciones con los mismos parámetros producen listas idénticas. `@settings(max_examples=100)`. **Validates: Requirements 5.4**
    - **Property 9: MCG rechaza parámetros inválidos** — cualquier combinación de parámetros inválidos lanza `ValueError`. `@settings(max_examples=100)`. **Validates: Requirements 2.6, 2.7, 2.8, 2.9, 5.6**
    - _Requirements: 2.2, 2.3, 2.4, 2.6, 2.7, 2.8, 2.9, 5.2, 5.4, 5.6_

  - [ ]* 4.3 Escribir tests de ejemplo para `congruencial_multiplicativo`
    - En `tests/test_congruencial_multiplicativo.py`, agregar:
      - `test_mcg_empty_on_zero_cantidad`: verifica que `cantidad=0` retorna `[]`. _Requirements: 2.5_
      - `test_mcg_passes_means_test`: 1000 valores con `a=16807`, `m=2**31-1`, semilla válida; verifica `pasa_prueba == True`. _Requirements: 2.10_
      - `test_mcg_passes_variance_test`: ídem con `prueba_varianza`. _Requirements: 2.11_

- [x] 5. Checkpoint — verificar MCG
  - Ejecutar `pytest tests/ --tb=short -q` desde `punto 3 - generadores/`.
  - Todos los tests (LCG + MCG) deben pasar antes de continuar.

- [x] 6. Implementar `generar_uniforme` en `src/generadores/distribuciones.py`
  - [x] 6.1 Escribir `generar_uniforme(metodo, parametros, cantidad) -> list[float]`
    - Importar `importlib` y resolver la función base mediante `importlib.import_module("src.generadores.<modulo>")` con `getattr` — o importar directamente `congruencial`.
    - Extraer `m = parametros["m"]` para la normalización.
    - Llamar al generador base con `**parametros` y `cantidad`; obtener la lista de enteros.
    - Normalizar: `r_i = X_i / m` para producir `list[float]` en `[0.0, 1.0)`.
    - Propagar cualquier `ValueError` del generador base sin capturarlo.
    - _Requirements: 3.1, 3.2, 3.4_

  - [ ]* 6.2 Escribir test de propiedad para `generar_uniforme` (Property 10)
    - En `tests/test_distribuciones.py`:
    - **Property 10: generar_uniforme produce floats en [0, 1)** — para `metodo ∈ {"congruencial_lineal", "congruencial_multiplicativo"}` con parámetros válidos y `n ≥ 1`, todos los valores son `float` en `[0.0, 1.0)`. `@settings(max_examples=100)`. **Validates: Requirements 3.2, 3.3**
    - _Requirements: 3.2, 3.3_

  - [ ]* 6.3 Escribir tests de ejemplo para `generar_uniforme`
    - `test_generar_uniforme_callable`: verifica que `generar_uniforme` existe y es callable (`cargar("src.generadores.distribuciones", "generar_uniforme") is not None`). _Requirements: 3.4_
    - `test_generar_uniforme_lcg_length`: verifica que el resultado tiene exactamente `cantidad` elementos. _Requirements: 3.2_
    - `test_generar_uniforme_mcg_length`: ídem para MCG. _Requirements: 3.3_

- [x] 7. Checkpoint final — suite completa y smoke test
  - Ejecutar `pytest tests/ --tb=short -q` desde `punto 3 - generadores/`.
  - Verificar que el smoke test existente `test_modulo_importable` también pasa para `src.generadores.congruencial` y `src.generadores.distribuciones`.
  - Todos los tests deben pasar; resolver cualquier fallo antes de terminar.

## Notes

- Las sub-tareas marcadas con `*` son opcionales y pueden saltarse para un MVP rápido.
- `hypothesis` debe añadirse a `requirements.txt` antes de ejecutar cualquier test de propiedad (tarea 1).
- Los generadores base retornan `list[int]`; la normalización a `[0, 1)` vive exclusivamente en `generar_uniforme` — no en `congruencial.py`.
- Los mensajes de error de cada `ValueError` ya están detallados en el documento de diseño; copiarlos literalmente garantiza consistencia con la interfaz Streamlit.
- Durante la implementación de la recurrencia, mantener las variables como `int` en todo momento; solo hacer `/ m` al construir la lista de floats en `generar_uniforme`.
- Para los tests estadísticos (`means_test`, `prueba_varianza`) se puede importar directamente desde `src.validacion.prueba_medias` y `src.validacion.prueba_varianza`.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["2.2", "2.3", "4.1"] },
    { "id": 3, "tasks": ["4.2", "4.3", "6.1"] },
    { "id": 4, "tasks": ["6.2", "6.3"] }
  ]
}
```
