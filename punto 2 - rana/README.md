# Punto 2 — Simulación de la rana (caminata aleatoria 1D)

Simulación de caminatas aleatorias simétricas en 1D por lotes encadenados.

---

## Formas de correrlo

### 1. Corrida por defecto

    cd "punto 2 - rana"
    python rana_1d.py

Corre 100 réplicas × 1.000.000 de pasos con semilla base `12345`.

### 2. Corrida con trayectorias

    python rana_1d.py --trayectorias

Igual que la anterior, pero además genera el gráfico de trayectorias.

### 3. Corrida corta (pruebas rápidas)

    python rana_1d.py --n_pasos 10000 --n_rep 20

Corre 20 réplicas × 10.000 pasos. Tarda segundos.

### 4. Cambiar la semilla base

    python rana_1d.py --semilla 777

Usa `777` como semilla base para generar las 100 réplicas.

### 5. Cambiar el número de réplicas

    python rana_1d.py --n_rep 500

Corre 500 réplicas en lugar de 100.

### 6. Cambiar el tamaño de lote

    python rana_1d.py --n_lote 500

Usa lotes de 500 pasos en lugar de 1000.

### 7. Cargar semillas desde archivo

    python rana_1d.py --archivo_semillas semillas.txt --n_rep 100

El archivo debe tener una semilla por línea (o separadas por comas,
puntos y coma, o espacios). Ejemplo `semillas.txt`:

    12345
    67890
    11111
    22222

### 8. Cambiar la carpeta de salida

    python rana_1d.py --salida resultados/prueba1

Guarda PNG y CSV en `resultados/prueba1/` en vez de `outputs/`.

### 9. Solo verificar equivalencia (lotes vs. continuo)

    python rana_1d.py --solo_verificar

Corre solo la verificación y termina. Útil para confirmar que la
estrategia de lotes encadenados está bien implementada.

### 10. Ver la ayuda completa

    python rana_1d.py --help

Muestra todos los parámetros disponibles con su descripción.

---

## Parámetros disponibles

| Argumento | Tipo | Default | Descripción |
|---|---|---|---|
| `--semilla` | int | `12345` | Semilla base. Las réplicas usan semillas Weyl derivadas de esta. |
| `--n_rep` | int | `100` | Número de réplicas independientes. |
| `--n_pasos` | int | `1_000_000` | Pasos por réplica. |
| `--n_lote` | int | `1000` | Tamaño de cada lote (pasos por lote). |
| `--archivo_semillas` | str | `None` | Ruta a `.txt` o `.csv` con semillas. Si se da, ignora `--semilla`. |
| `--salida` | str | `"outputs"` | Carpeta donde se guardan los resultados. |
| `--solo_verificar` | flag | off | Corre solo la verificación de equivalencia y termina. |
| `--trayectorias` | flag | off | Genera además el gráfico de trayectorias. |

---

## Combinaciones típicas

Corrida oficial del taller:

    python rana_1d.py --n_pasos 1000000 --n_rep 100 --trayectorias

Prueba rápida con semilla distinta:

    python rana_1d.py --semilla 42 --n_pasos 10000 --n_rep 50

Corrida con semillas externas:

    python rana_1d.py --archivo_semillas semillas_ejemplo.txt --n_rep 100 --n_pasos 1000000

Guardar en carpeta separada:

    python rana_1d.py --salida outputs/corrida_oficial

---

## Qué produce cada corrida

### Salida en consola

    Iniciando simulación principal...
    ============================================================
    Réplicas: 100 | pasos: 1000000
    Media: ... (teórica 0)
    Desv. est.: ... (teórica 1000.00)
    Mín/Máx: ... / ...
    Dentro de ±1σ: ... (normal: 68.3%)
    Dentro de ±2σ: ... (normal: 95.4%)
    Paridad correcta: True
    ============================================================
    Retorno exacto en paso 1000: ... (teórico 0.0252)
    Paso por el origen en ≤1000: ... (teórico 0.9748)
    Tiempo: ... s

### Archivos generados

| Archivo | Cuándo se genera | Qué contiene |
|---|---|---|
| `outputs/histograma_1d.png` | Siempre | Histograma de posiciones finales + curva normal teórica. |
| `outputs/trayectorias_1d.png` | Con `--trayectorias` | 10 trayectorias de ejemplo. |
| `outputs/finales_1d.csv` | Siempre | Tabla con réplica, semilla, posición final. |

---

## Cómo ver los resultados

Desde la terminal:

    xdg-open outputs/histograma_1d.png

Desde VS Code: navega a `outputs/` en el panel izquierdo y haz doble
clic en el PNG.

Desde el explorador de archivos: abre la carpeta `outputs/` y haz doble
clic en el PNG.

---

## Descripción del algoritmo

### Idea general

La rana parte del origen (posición 0). En cada paso:

- `Ri < 0.5` → paso `+1` (adelante)
- `Ri >= 0.5` → paso `-1` (atrás)

Tras `n_pasos` pasos, la posición final es la suma acumulada.

### Lotes encadenados

En vez de simular 1.000.000 de pasos de un solo golpe, se divide en
lotes de `n_lote` pasos. El estado que pasa de un lote al siguiente es:

1. Posición final del lote anterior → posición inicial del siguiente.
2. Estado del generador → continúa la secuencia pseudoaleatoria.
3. Flag `visito` → si la rana ya tocó el origen.

Correr en 1 lote grande o en muchos lotes pequeños da el mismo resultado.
Verificar con:

    python rana_1d.py --solo_verificar

### Semillas independientes

Las réplicas usan semillas separadas por la constante `2654435761`:

    semilla_i = (semilla_base + i * 2654435761) mod 2^32

Esto garantiza que las semillas estén bien separadas entre sí.

---

## Estructura de la carpeta

    punto 2 - rana/
    ├── rana_1d.py          ← simulación completa
    ├── README.md           ← este archivo
    └── outputs/            ← se crea al correr
        ├── histograma_1d.png
        ├── trayectorias_1d.png
        └── finales_1d.csv

---

## Cambiar de generador

El único punto a modificar es `crear_generador` dentro de `rana_1d.py`:

    def crear_generador(semilla):
        from generadores.congruencial import congruencial_lineal
        return GeneradorConectado(
            funcion=congruencial_lineal,
            m=2**32,
            semilla=semilla,
            a=1664525,
            c=1013904223,
            m=2**32,
        )

La firma asumida del generador es:

    funcion(semilla, ..., cantidad) -> list[int]

donde `cantidad` es cuántos enteros debe generar.

---

## Notas para la extensión a 2D y 3D

Para generalizar a 2D y 3D:

1. La posición pasa de `int` a vector.
2. El paso pasa de `+1/-1` a vector unitario aleatorio.
3. El histograma solo aplica en 1D. En 2D/3D se usan scatter plots.
4. La paridad solo aplica en 1D.
5. La lógica de lotes encadenados es idéntica en todas las dimensiones.