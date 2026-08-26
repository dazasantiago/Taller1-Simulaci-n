# Taller 1 - Simulación: Generadores y Validación de Números Pseudoaleatorios

Biblioteca en Python para generar números pseudoaleatorios **implementados
desde cero** (sin usar `random`, `numpy.random` ni ninguna librería de
generación aleatoria del lenguaje) y validarlos mediante pruebas
estadísticas clásicas.

> Estado del proyecto: **esqueleto inicial**. Las funciones están
> definidas (firmas + docstrings) pero su lógica aún no está
> implementada (lanzan `NotImplementedError`). Ver la sección
> "Estructura del proyecto" y `docs/README.md` para el detalle.

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

## Requisitos

- Python 3.10 o superior.
- Git.

## Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Taller1
```

## Crear y activar el entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

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

Para desactivar el entorno virtual en cualquier plataforma: `deactivate`.

## Instalar dependencias

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

## Ejecutar las pruebas (pytest)

```bash
pytest
```

Actualmente solo existe una prueba de humo (`tests/test_placeholder.py`)
que verifica que todos los módulos se puedan importar sin errores.

## Uso de la CLI (esqueleto)

```bash
python main.py                # abre el menú interactivo (pendiente de implementar)
python main.py generar --help # ver argumentos del subcomando de generación
python main.py validar --help # ver argumentos del subcomando de validación
```

La lógica real de generación/validación todavía no está implementada;
ver `main.py` para el detalle de los argumentos definidos.

## Estructura del proyecto

```
Taller1/
├── main.py                    # Punto de entrada CLI / menú interactivo
├── requirements.txt
├── pytest.ini
├── .gitignore
├── src/
│   ├── generadores/
│   │   ├── cuadrados_medios.py    # Método de Cuadrados Medios
│   │   ├── congruencial.py        # Lineal, Multiplicativo, Aditivo
│   │   └── distribuciones.py      # Uniforme y Normal (Box-Muller)
│   └── validacion/
│       └── pruebas_estadisticas.py # Medias, Varianza, Chi², KS, Póker, Rachas
├── data/
│   └── seeds/                     # Semillas de ejemplo (.txt / .csv)
├── tests/
│   └── test_placeholder.py        # Smoke test de importación
├── docs/
│   └── README.md                  # Documentación técnica de la biblioteca
└── outputs/                       # Gráficos/histogramas generados (vacío, .gitkeep)
```

## Convención de branches (equipo de 5 personas)

Como varias personas van a trabajar sobre funciones distintas dentro de
los mismos archivos (ej. las 3 funciones de `congruencial.py`, o las 6
pruebas de `pruebas_estadisticas.py`), se recomienda:

- **`main`**: rama estable. Solo se mergea vía Pull Request revisado.
- **Ramas de feature por función**, no por persona ni por archivo
  completo. Nomenclatura sugerida:
  `feature/<area>-<funcion>`, por ejemplo:
  - `feature/generadores-cuadrados-medios`
  - `feature/generadores-congruencial-lineal`
  - `feature/validacion-prueba-poker`
  - `feature/cli-lectura-semillas`
- Otros prefijos: `fix/...` (corrección de bug), `docs/...`
  (documentación), `test/...` (pruebas).

**Reglas para minimizar conflictos de merge en los mismos archivos:**

1. Cada rama debe tocar **solo la función que le corresponde** (y, si
   aplica, su prueba unitaria). Evitar tocar funciones de compañeros en
   la misma rama.
2. Hacer **Pull Requests pequeños y frecuentes** en lugar de ramas
   largas que acumulen muchos cambios: cuanto menos tiempo viva una
   rama, menor la probabilidad de conflicto.
3. Actualizar la rama contra `main` seguido (`git pull --rebase origin main`)
   antes de abrir o actualizar un PR.
4. **No reformatear código que no se está modificando** (evitar que un
   formateador reescriba archivos completos y genere conflictos
   artificiales).
5. Revisión cruzada: al menos una aprobación de otro integrante antes
   de mergear a `main`.
6. Si dos personas necesitan tocar el mismo archivo al mismo tiempo,
   coordinarse para que una termine y mergee antes de que la otra
   empiece (o resolver el conflicto en pareja apenas aparezca, sin
   dejarlo acumular).
