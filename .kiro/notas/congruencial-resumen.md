# Implementación de Generadores Congruenciales — Resumen técnico

## Qué se implementó

### `src/generadores/congruencial.py`

Dos generadores de números pseudoaleatorios implementados desde cero en Python puro,
sin ninguna librería de aleatoriedad (`random`, `numpy.random`, etc.).

#### `linear_congruential(seed, a, c, m, count) -> list[int]`

Implementa el **Generador Congruencial Lineal (LCG)** mediante la recurrencia:

```
X_{n+1} = (a * X_n + c) mod m
```

| Parámetro | Descripción | Restricción |
|-----------|-------------|-------------|
| `seed`    | Valor inicial X_0 | [0, m-1] |
| `a`       | Multiplicador | [1, m-1] |
| `c`       | Incremento | [0, m-1] |
| `m`       | Módulo | > 1 |
| `count`   | Cantidad de valores | <= 0 retorna lista vacía |

Parámetros de referencia (Numerical Recipes / Knuth): `a=1664525`, `c=1013904223`, `m=2^32`.
Con estos parámetros se cumple el **Teorema de Dobell** (período completo = m).

#### `multiplicative_congruential(seed, a, m, count) -> list[int]`

Implementa el **Generador Congruencial Multiplicativo (MCG)**, caso especial del LCG con `c = 0`:

```
X_{n+1} = (a * X_n) mod m
```

| Parámetro | Descripción | Restricción |
|-----------|-------------|-------------|
| `seed`    | Valor inicial X_0 | > 0, no múltiplo de m |
| `a`       | Multiplicador | >= 1 |
| `m`       | Módulo | > 1 |
| `count`   | Cantidad de valores | <= 0 retorna lista vacía |

Parámetros de referencia (Park-Miller / MINSTD): `a=16807`, `m=2^31-1`.
Período máximo posible: `m-1 = 2^31-2` (m es primo de Mersenne).

Ambas funciones validan sus parámetros y lanzan `ValueError` con mensajes descriptivos
antes de ejecutar la recurrencia.

---

### `src/generadores/distribuciones.py`

Capa de normalización y transformación sobre los generadores base.

#### `generate_uniform(method, parameters, count) -> list[float]`

Convierte la secuencia entera X_i en valores uniformes R_i en [0.0, 1.0):

```
R_i = X_i / m
```

Recibe el nombre del generador como string (`"congruencial_lineal"` o
`"congruencial_multiplicativo"`) y lo resuelve en tiempo de ejecución via
`importlib`, siguiendo el contrato del catálogo de la aplicación.

#### `generate_normal(base_method, parameters, count) -> list[float]`

Genera valores N_i ~ N(0,1) aplicando la **transformada de Box-Muller** sobre
pares de uniformes R_i producidos por `generate_uniform`:

```
R = sqrt(-2 * ln(U1))
Z1 = R * cos(2π * U2)
Z2 = R * sin(2π * U2)
```

---

## Arquitectura del módulo

```
app/catalogo.py          <- único punto de entrada de la UI a src/
    |
    v  (importlib en tiempo de ejecución)
src/generadores/
    distribuciones.py    <- R_i (uniformes) y N_i (normales)
        |
        v
    congruencial.py      <- X_i (enteros crudos, aritmética pura)
```

Los generadores base devuelven enteros (`list[int]`). La normalización
ocurre exclusivamente en `distribuciones.py`. Esto permite reutilizar
los generadores en otros contextos sin forzar normalización.

---

## Pendiente para completar el punto 3

| Item | Estado | Responsable |
|------|--------|-------------|
| Cuadrados Medios | ✅ Implementado (PR #3, Laura) | Compañera |
| Congruencial Lineal | ✅ Implementado | Este archivo |
| Congruencial Multiplicativo | ✅ Implementado | Este archivo |
| Congruencial Aditivo | ⏳ Stub vacío | Por asignar |
| generar_uniforme (R_i) | ✅ Implementado | Este archivo |
| generar_normal / Box-Muller (N_i) | ✅ Implementado | Este archivo |
| Pruebas estadísticas (6) | ✅ Ya existían | Proyecto base |
| UI Streamlit | ✅ Ya existía | Proyecto base |

---

## Pendientes de entregable (informe)

Estos ítems requieren acción manual para el informe final:

- [ ] **Capturas de pantalla**: histograma de LCG, histograma de MCG, resultado de al menos una prueba estadística completa, y carga de semillas desde archivo.
- [ ] **Archivo de semillas ejemplo** (`.txt` o `.csv`) en la carpeta `data/`.
- [ ] **Cuadro técnico**: lenguaje Python 3.x, SO, procesador y memoria RAM del equipo.
- [ ] **README del módulo**: actualizar `docs/README.md` o `README.md` con descripción de funciones, parámetros y ejemplos de uso.
