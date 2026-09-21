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
