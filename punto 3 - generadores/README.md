# Taller 1 - Simulación: Generadores y Validación de Números Pseudoaleatorios

Biblioteca en Python para generar números pseudoaleatorios **implementados
desde cero** (sin usar `random`, `numpy.random` ni ninguna librería de
generación aleatoria del lenguaje) y validarlos mediante pruebas
estadísticas clásicas.

> **Estado del proyecto:** solo está montada la estructura (carpetas,
> configuración, archivos placeholder). Ninguna función está
> implementada todavía — eso es justamente el trabajo del equipo. Ver
> "Arquitectura y flujo" abajo y `docs/README.md` para el contrato
> (firma y retorno esperado) de cada función a implementar.

## Contenido

- Generadores: Cuadrados Medios, Congruencial Lineal, Congruencial
  Multiplicativo, Congruencial Aditivo, distribución Uniforme y
  distribución Normal (Box-Muller) derivadas de los anteriores.
- Validación estadística: prueba de medias, prueba de varianza, prueba
  Chi-cuadrado, prueba de Kolmogorov-Smirnov (KS), prueba de Póker y
  prueba de rachas.

Pensado como **biblioteca reutilizable**: este módulo será importado
más adelante por otros dos proyectos de simulación (caminatas
aleatorias y un modelo Montecarlo tipo SEIR), que no forman parte de
este repositorio.

## Arquitectura y flujo

Capas del módulo (cada una depende solo de la anterior):

```
data/seeds/  ─┐
              ▼
src/generadores/                       (enteros crudos)
  cuadrados_medios.py, congruencial.py
              │
              ▼
src/generadores/distribuciones.py      (normaliza a [0,1) / Normal)
  generar_uniforme, generar_normal
              │
              ▼
src/validacion/prueba_*.py (recibe list[float], calcula estadístico + gráfico)
              │
              ▼
main.py                                 (CLI/menú que orquesta todo lo anterior)
```

- `src/generadores/` debe contener funciones **puras** (mismo input ⇒
  mismo output, sin `print` ni efectos secundarios).
- `src/validacion/` no depende de cómo se generó la secuencia: solo
  recibe una `list[float]` y devuelve el resultado de la prueba.
- `main.py` es la capa de orquestación: lee semillas/parámetros,
  llama al generador elegido y luego a la(s) prueba(s) elegida(s).
- `outputs/` es donde deberían guardarse los gráficos que generen las
  pruebas estadísticas.
- `docs/README.md` documenta el **contrato** de cada función (firma y
  qué debe retornar) — es la referencia a seguir al implementar, y lo
  que usarán los futuros proyectos que importen esta biblioteca.

Ahora mismo nada de esto está implementado: todos los archivos de
`src/` y `main.py` son placeholders con un comentario indicando qué va
en cada uno. `pytest` solo confirma que los módulos importan sin
errores de sintaxis.

## Requisitos

- Python 3.10 o superior.
- Git.

## ¿Cómo funciona el entorno virtual (venv)?

Un **venv** es una copia aislada del intérprete de Python y sus
librerías, separada de la instalación global de Python de tu equipo.
Sirve para que las versiones de `numpy`, `scipy`, `matplotlib`, etc. de
este proyecto no choquen con las que ya tengas instaladas para otras
materias o proyectos.

Al correr `python -m venv venv` se crea una carpeta `venv/` con su
propio ejecutable de Python y su propia carpeta de librerías (vacía al
inicio). Al **activarlo**, la terminal actual apunta temporalmente a
ese Python aislado en vez del del sistema — por eso el prompt cambia a
mostrar `(venv)`. Desde ese momento, `pip install` instala solo dentro
de esa carpeta.

**Qué se comparte y qué no:**

- La carpeta `venv/` **nunca se sube a git** (está en `.gitignore`): es
  pesada, depende del sistema operativo de cada quien, y no tiene
  sentido compartirla.
- Lo que sí se comparte por git es `requirements.txt`: la "receta" con
  las versiones exactas de cada librería. Así, aunque cada quien tenga
  su propio `venv/` local, todos terminan con las mismas versiones
  instaladas y el código se comporta igual en las 5 máquinas.

**Qué debe hacer cada integrante (en su propia máquina, una sola vez):**

Los pasos 1-3 de la guía de abajo los repite cada una de las 5 personas,
de forma independiente, la primera vez que configura el proyecto. El
`venv/` que crean queda viviendo solo en su disco; si alguien clona el
repo en otra máquina, simplemente repite esos pasos ahí.

**Qué debe recordar cada quien día a día:**

- Cada vez que abran una terminal nueva para trabajar en el proyecto,
  deben volver a activar el venv (no queda activado permanentemente) —
  si no ven `(venv)` en el prompt, no está activo.
- Si alguien agrega una librería nueva al proyecto, debe actualizar
  `requirements.txt` y avisar al equipo para que todos reinstalen.
- El venv es local: no afecta ni es afectado por el trabajo de sus
  compañeros. Lo único compartido entre los 5 es el código (vía git) y
  `requirements.txt`.

## Guía rápida para empezar a trabajar

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Taller1
```

### 2. Crear el entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea la ejecución de scripts, corre una vez (como
> usuario, no hace falta admin):
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**Windows (cmd):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux (bash/zsh):**

```bash
python3 -m venv venv
source venv/bin/activate
```

Sabrás que quedó activado porque el prompt de tu terminal empieza con
`(venv)`. Para desactivarlo en cualquier plataforma: `deactivate`.

### 3. Instalar dependencias

Con el entorno virtual **activado**:

```bash
pip install -r requirements.txt
```

### 4. Verificar que todo quedó bien

```bash
pytest
```

Debería mostrar todos los tests en verde (hoy solo hay un smoke test
que verifica que los módulos importen sin errores).

## Uso de la CLI

```bash
python main.py
```

`main.py` es por ahora solo un placeholder (sin lógica ni argumentos
todavía) — se irá construyendo a medida que el equipo implemente los
generadores y las pruebas.

## Interfaz gráfica (en desarrollo)

Además de la CLI, el proyecto tendrá más adelante una interfaz gráfica
construida con [Streamlit](https://streamlit.io/), en la carpeta
`/app` (separada de `/src`). **La implementación todavía está
pendiente** — hoy `app/main.py` es solo un placeholder (título +
comentarios TODO); ver `app/README.md` para el detalle de qué debería
permitir hacer la interfaz una vez construida.

- **Instalación**: ya incluida en `requirements.txt` (`streamlit`), se
  instala junto con el resto de dependencias (paso 3 de la guía
  rápida).
- **Cómo correrla** (una vez que haya algo implementado):
  ```bash
  streamlit run app/main.py
  ```

## Estructura del proyecto

```
Taller1/
├── main.py                    # Punto de entrada CLI / menú (placeholder)
├── requirements.txt
├── pytest.ini
├── .gitignore
├── src/
│   ├── generadores/
│   │   ├── cuadrados_medios.py    # Método de Cuadrados Medios
│   │   ├── congruencial.py        # Lineal, Multiplicativo, Aditivo
│   │   └── distribuciones.py      # Uniforme y Normal (Box-Muller)
│   └── validacion/
│       ├── prueba_medias.py
│       ├── prueba_varianza.py
│       ├── prueba_chi_cuadrado.py
│       ├── prueba_kolmogorov_smirnov.py
│       ├── prueba_poker.py
│       └── prueba_rachas.py
├── app/
│   ├── main.py                    # Interfaz Streamlit (placeholder, pendiente)
│   └── README.md                  # Qué debe permitir hacer la interfaz
├── data/
│   └── seeds/                     # Semillas de ejemplo (.txt / .csv)
├── tests/
│   └── test_placeholder.py        # Smoke test de importación
├── docs/
│   └── README.md                  # Contrato/API de la biblioteca
└── outputs/                       # Gráficos/histogramas generados (vacío, .gitkeep)
```

## Recursos

- `docs/README.md`: contrato de cada función (firma, parámetros, tipo
  de retorno) y convenciones a respetar para que el módulo sea
  reutilizable por los próximos proyectos.


## Punto 3 — Generadores Congruenciales

### Qué pide y por qué

El punto 3 exige construir generadores de números pseudoaleatorios desde cero — sin `random`, `numpy.random` ni ninguna librería de aleatoriedad. La razón es demostrar que se entiende el algoritmo, no solo que se sabe llamar una función. Los métodos congruenciales son los más usados en simulación clásica precisamente porque su mecánica es explícita y analizable.

### Cómo funciona el flujo completo

```
semilla (X_0)
    ↓
congruencial.py  →  X_i  (enteros en [0, m))
    ↓
distribuciones.py  →  R_i = X_i / m  (uniformes en [0.0, 1.0))
    ↓
distribuciones.py  →  N_i  (normales vía Box-Muller, si se necesitan)
    ↓
pruebas estadísticas  (reciben list[float] de R_i)
```

### Generador Congruencial Lineal (LCG)

Recurrencia: `X_{n+1} = (a * X_n + c) mod m`

Genera enteros `X_i` en `[0, m)`. La semilla `X_0` debe estar en `[0, m-1]`.

Parámetros usados — ANSI C (ISO/IEC 9899:1990): `a = 1103515245`, `c = 12345`, `m = 2**31`.
Con estos tres valores se cumple el **Teorema de Dobell**, que garantiza período completo igual a `m`: `mcd(c, m) = 1`, `a-1` divisible por todos los factores primos de `m`, y `a-1` divisible por 4 porque `m` es divisible por 4.

Restricciones que valida el código:
- `m > 1`
- `a` en `[1, m-1]`
- `c` en `[0, m-1]`
- `seed` en `[0, m-1]`

### Generador Congruencial Multiplicativo (MCG)

Recurrencia: `X_{n+1} = (a * X_n) mod m`  — caso especial del LCG con `c = 0`.

Con `c = 0` el período nunca puede ser completo (Dobell no aplica), pero si `m` es primo y `a` es raíz primitiva módulo `m`, el período es `m - 1`, que es el máximo posible.

Parámetros usados — L'Ecuyer (1988), CACM: `a = 48271`, `m = 2**31 - 1`.
`m = 2147483647` es primo de Mersenne (2³¹ − 1). L'Ecuyer demostró que `a = 48271` tiene mejores propiedades espectrales que el `a = 16807` original de Park & Miller (1988).

Restricciones que valida el código:
- `m > 1`
- `a >= 1`
- `seed > 0`
- `seed` no múltiplo de `m` (produciría secuencia degenerada de ceros)

### Qué generan y qué tener en cuenta

Ambas funciones retornan `list[int]` — enteros crudos en `[0, m)`, **no** valores en `[0, 1)`. La normalización `R_i = X_i / m` la hace `distribuciones.py`, no el generador. Esto permite reutilizar los enteros en otros contextos sin forzar normalización.

Cosas a tener en cuenta al usar:
- Con parámetros distintos a los de referencia el período puede ser mucho menor que `m` y el histograma se verá no uniforme aunque el código sea correcto.
- La semilla determina completamente la secuencia — misma semilla, mismos números siempre. Para comparar dos generadores usar la misma semilla.
- Aumentar la cantidad de números generados hace que el histograma converja más rápido a la distribución uniforme teórica (Ley de los Grandes Números).
- Las pruebas estadísticas reciben `list[float]` con valores en `[0, 1)`, no los enteros del generador. Siempre pasar primero por `distribuciones.py`.
