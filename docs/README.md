# Documentación técnica: biblioteca de generación y validación de números pseudoaleatorios

Este documento describe el módulo (`src/`) pensado como **biblioteca
reutilizable**, para que el equipo actual lo implemente de forma
consistente y para que los futuros proyectos que lo consuman (caminatas
aleatorias y un modelo Montecarlo tipo SEIR — no incluidos en este
repositorio todavía) sepan qué importar y qué esperar de cada función.

## Propósito del módulo

Proveer, en un solo lugar, generadores de números pseudoaleatorios
implementados **desde cero** (sin `random`, `numpy.random` ni ninguna
otra librería de generación aleatoria del lenguaje) y las pruebas
estadísticas necesarias para validar la calidad de esas secuencias.
Los proyectos consumidores deberán poder generar números uniformes o
normales sin preocuparse por el algoritmo interno, y validar cualquier
secuencia (propia o externa) con las 6 pruebas incluidas.

## Cómo se espera que se importe

Mientras el módulo no esté empaquetado formalmente (no hay `pyproject.toml`
ni publicación a un índice de paquetes en este repositorio), los
proyectos consumidores deberán agregar la raíz de este repositorio a su
`PYTHONPATH` (o copiar/enlazar `src/` dentro de su propio proyecto) e
importar directamente los submódulos, por ejemplo:

```python
from src.generadores.cuadrados_medios import cuadrados_medios
from src.generadores.congruencial import (
    congruencial_lineal,
    congruencial_multiplicativo,
    congruencial_aditivo,
)
from src.generadores.distribuciones import generar_uniforme, generar_normal
from src.validacion.pruebas_estadisticas import (
    prueba_medias,
    prueba_varianza,
    prueba_chi_cuadrado,
    prueba_ks,
    prueba_poker,
    prueba_rachas,
)
```

> Nota: si más adelante se decide empaquetar formalmente el módulo
> (`pyproject.toml` / `setup.py` para poder hacer `pip install`), esa
> configuración se agregará cuando exista un consumidor real que lo
> requiera; no forma parte del alcance actual del repositorio.

## Contrato de cada función

El detalle completo de parámetros, tipos y comportamiento esperado vive
en el docstring de cada función (son la fuente de verdad); aquí se deja
un resumen de firmas y retornos para referencia rápida.

### Generadores (`src/generadores/`)

| Función | Firma | Retorno esperado |
|---|---|---|
| Cuadrados Medios | `cuadrados_medios(semilla: int, n_digitos: int, cantidad: int)` | `list[int]` — valores enteros de `n_digitos` dígitos, sin normalizar |
| Congruencial Lineal | `congruencial_lineal(semilla: int, a: int, c: int, m: int, cantidad: int)` | `list[int]` — valores en `[0, m)`, sin normalizar |
| Congruencial Multiplicativo | `congruencial_multiplicativo(semilla: int, a: int, m: int, cantidad: int)` | `list[int]` — valores en `[0, m)`, sin normalizar |
| Congruencial Aditivo | `congruencial_aditivo(semillas_iniciales: list[int], m: int, cantidad: int)` | `list[int]` — valores en `[0, m)`, sin normalizar |
| Uniforme | `generar_uniforme(metodo: str, parametros: dict, cantidad: int)` | `list[float]` — valores en `[0, 1)` |
| Normal | `generar_normal(metodo_base: str, parametros: dict, cantidad: int)` | `list[float]` — valores ~Normal(media, desviación²), estándar por defecto |

Los generadores "base" (Cuadrados Medios y los tres congruenciales)
devuelven **enteros sin normalizar**; la normalización a `[0, 1)`
ocurre en `generar_uniforme`, que es la función que los proyectos
consumidores deberían usar en la mayoría de los casos (junto con
`generar_normal` cuando necesiten valores normales).

### Validación (`src/validacion/pruebas_estadisticas.py`)

| Función | Firma | Retorno esperado |
|---|---|---|
| Medias | `prueba_medias(secuencia: list[float], nivel_confianza: float)` | `dict` (ver contrato común) |
| Varianza | `prueba_varianza(secuencia: list[float], nivel_confianza: float)` | `dict` (ver contrato común) |
| Chi-cuadrado | `prueba_chi_cuadrado(secuencia: list[float], n_intervalos: int)` | `dict` (+ `frecuencias_observadas`, `frecuencias_esperadas`) |
| Kolmogorov-Smirnov | `prueba_ks(secuencia: list[float])` | `dict` (ver contrato común) |
| Póker | `prueba_poker(secuencia: list[float], tam_mano: int)` | `dict` (+ `categoria_frecuencias`) |
| Rachas | `prueba_rachas(secuencia: list[float])` | `dict` (+ `num_rachas`) |

**Contrato común de retorno** para las 6 pruebas (`dict`):

```python
{
    "estadistico": float,                  # estadístico de prueba calculado
    "valor_critico": float | None,         # valor crítico teórico/tabla (si aplica)
    "valor_p": float | None,               # p-valor (si aplica)
    "pasa_prueba": bool,                   # True si no se rechaza H0
    "figura": matplotlib.figure.Figure,    # gráfico generado por la prueba
}
```

Cada prueba agrega, además, las llaves específicas indicadas en la
tabla y en su docstring (ver `src/validacion/pruebas_estadisticas.py`
para el detalle de qué gráfico debe producir cada una).

## Convenciones que deben respetarse como biblioteca

Para que el módulo sea consumible sin sorpresas desde otros proyectos:

- Las funciones de `src/generadores/` deben ser **puras y
  deterministas**: mismos parámetros de entrada ⇒ misma secuencia de
  salida (no deben depender de estado global ni de `random`/`numpy.random`).
- No deben imprimir por consola ni tener otros efectos secundarios;
  deben limitarse a recibir parámetros y retornar la secuencia
  generada.
- Deben devolver siempre listas de tipos simples (`list[int]` /
  `list[float]`), no generadores/iteradores, para que el consumidor
  pueda reutilizar el resultado sin preocuparse por el agotamiento del
  iterador.
- Las funciones de `src/validacion/` pueden generar gráficos
  (`matplotlib`) pero deben devolverlos como parte del `dict` de
  resultado (llave `"figura"`) en lugar de guardarlos a disco o
  mostrarlos directamente; guardar/mostrar es responsabilidad del
  punto de entrada (`main.py`) o del proyecto consumidor.

## Pendientes (fuera del alcance de este repositorio por ahora)

- Implementación real de la lógica de generadores y pruebas (este
  repositorio solo define la estructura y los esqueletos).
- Empaquetado formal (`pyproject.toml`) si/cuando los proyectos de
  caminatas aleatorias y Montecarlo SEIR lo requieran como dependencia
  instalable.
