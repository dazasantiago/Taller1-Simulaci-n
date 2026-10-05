# Punto 2 — Simulación 2D de la rana (caminata aleatoria en el plano)

Simulación de caminatas aleatorias simétricas en 2D por lotes encadenados.
La rana se mueve en 4 direcciones (arriba, abajo, izquierda, derecha), cada
una con probabilidad 0.25. Usa los generadores y las pruebas del Punto 3.

---

## Requisitos

Python 3.12+, `numpy`, `matplotlib`, `scipy`,
`pandas`. El venv del repo ya los tiene.

---

## Formas de correrlo

### 1. Validar el conjunto (6 pruebas del Punto 3)

    python rana_2d.py --validar

Debe terminar con `TODO OK` (con generador multiplicativo).

### 2. Corrida oficial del taller

    python rana_2d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100 --trayectorias

Simula 100 réplicas × 1.000.000 de pasos en 2D. Genera:
- `outputs/2d/scatter_2d.png`
- `outputs/2d/trayectorias_2d.png`
- `outputs/2d/finales_2d.csv`

### 4. Corrida corta (pruebas rápidas)

    python rana_2d.py --n_pasos 10000 --n_rep 20

### 5. Cambiar la semilla

    python rana_2d.py --semilla 777

### 6. Guardar en carpeta separada

    python rana_2d.py --salida outputs/2d_prueba

---

## Parámetros disponibles

| Argumento | Tipo | Default | Descripción |
|---|---|---|---|
| `--semilla` | int | `12345` | Semilla base. Las réplicas usan semillas derivadas. |
| `--n_rep` | int | `100` | Número de réplicas independientes. |
| `--n_pasos` | int | `1_000_000` | Pasos por réplica. |
| `--n_lote` | int | `1000` | Tamaño de cada lote. |
| `--generador` | str | `multiplicativo` | `cuadrados_medios`, `lineal` o `multiplicativo`. |
| `--archivo_semillas` | str | `None` | Ruta a `.txt`/`.csv` con semillas. |
| `--salida` | str | `outputs/2d` | Carpeta de salida. |
| `--validar` | flag | off | Corre validación del conjunto y termina. |
| `--solo_verificar` | flag | off | Corre equivalencia de lotes y termina. |
| `--trayectorias` | flag | off | Genera gráfico de trayectorias 2D. |

---

## Qué produce cada corrida

### Salida en consola (corrida normal)

    ============================================================
    Réplicas: 100 | pasos: 1000000 | dimensión: 2D
    Media x: ... (teórica 0)
    Media y: ... (teórica 0)
    Desv. x: ... (teórica 1000.00)
    Desv. y: ... (teórica 1000.00)
    Mín/Máx x: ... / ...
    Mín/Máx y: ... / ...
    Retorno al origen DESPUÉS del paso 1000: ...
    ============================================================
    Tiempo: ... s

### Archivos generados

| Archivo | Cuándo | Contiene |
|---|---|---|
| `<salida>/scatter_2d.png` | Siempre | Scatter plot de posiciones finales. |
| `<salida>/trayectorias_2d.png` | Con `--trayectorias` | 10 trayectorias en el plano. |
| `<salida>/finales_2d.csv` | Siempre | réplica, semilla, x_final, y_final, visito_despues. |

---

## Descripción del algoritmo

### Idea general

La rana parte del origen (0, 0). En cada paso elige una de 4 direcciones
con probabilidad 0.25 cada una:

- Derecha: (+1, 0)
- Izquierda: (−1, 0)
- Arriba: (0, +1)
- Abajo: (0, −1)

La decisión se hace con **un solo uniforme `R ∈ [0, 1)`** por paso:

- `R < 0.25` → derecha
- `0.25 ≤ R < 0.50` → izquierda
- `0.50 ≤ R < 0.75` → arriba
- `0.75 ≤ R < 1.00` → abajo

### Lotes encadenados

Igual que en 1D. El estado que pasa de un lote al siguiente es:

1. Posición final (x, y) del lote anterior.
2. Estado del generador.
3. Flag `visito_despues`: si ya volvió al origen después del paso 1000.

### Retorno al origen

El evento de interés es el **retorno exacto al origen (0, 0) en algún
momento después del paso 1000**, es decir entre los pasos 1001 y 1.000.000.
No se cuenta si la rana está en (0, 0) justo en el paso 1000.

---

## Visualizaciones

- **Scatter plot de posiciones finales**: adecuado en 2D porque muestra
  directamente la nube de puntos finales en el plano (x, y). Cada punto
  es una réplica.
- **Trayectorias 2D**: adecuado porque muestra el camino completo en el
  plano. Se grafican 10 réplicas para que el gráfico sea legible.

---

## Cambiar de generador

    python rana_2d.py --generador multiplicativo
    python rana_2d.py --generador lineal
    python rana_2d.py --generador cuadrados_medios

---

## Estructura de la carpeta

    punto 2 - rana/
    ├── rana_1d.py          ← simulación 1D
    ├── rana_2d.py          ← simulación 2D (este archivo)
    ├── rana_3d.py          ← simulación 3D (pendiente)
    ├── README.md           ← README general del 1D
    ├── README_2d.md        ← este archivo
    └── outputs/
        ├── 2d/
        │   ├── scatter_2d.png
        │   ├── trayectorias_2d.png
        │   └── finales_2d.csv
        └── ...

---