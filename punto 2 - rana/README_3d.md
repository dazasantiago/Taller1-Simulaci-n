# Punto 2 — Simulación 3D de la rana (caminata aleatoria en el espacio)

Simulación de caminatas aleatorias simétricas en 3D por lotes encadenados.
La rana se mueve en 6 direcciones (±x, ±y, ±z), cada una con probabilidad
1/6. Usa los generadores y las pruebas del Punto 3.

---

## Requisitos

python 3.12+, `numpy`,
`matplotlib`, `scipy`, `pandas`. El venv del repo ya los tiene.

---

## Formas de correrlo

### 1. Validar el conjunto (6 pruebas del Punto 3)

    python rana_3d.py --validar

Debe terminar con `TODO OK` (con generador multiplicativo).

### 2. Corrida oficial del taller

    python rana_3d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100 --trayectorias

Simula 100 réplicas × 1.000.000 de pasos en 3D. Genera:
- `outputs/3d/scatter_3d.png`
- `outputs/3d/proyecciones_3d.png`
- `outputs/3d/trayectorias_3d.png`
- `outputs/3d/finales_3d.csv`

### 4. Corrida corta (pruebas rápidas)

    python rana_3d.py --n_pasos 10000 --n_rep 20

### 5. Cambiar la semilla

    python rana_3d.py --semilla 777

### 6. Guardar en carpeta separada

    python rana_3d.py --salida outputs/3d_prueba

---

## Parámetros disponibles

| Argumento | Tipo | Default | Descripción |
|---|---|---|---|
| `--semilla` | int | `12345` | Semilla base. |
| `--n_rep` | int | `100` | Número de réplicas independientes. |
| `--n_pasos` | int | `1_000_000` | Pasos por réplica. |
| `--n_lote` | int | `1000` | Tamaño de cada lote. |
| `--generador` | str | `multiplicativo` | `cuadrados_medios`, `lineal` o `multiplicativo`. |
| `--archivo_semillas` | str | `None` | Ruta a `.txt`/`.csv` con semillas. |
| `--salida` | str | `outputs/3d` | Carpeta de salida. |
| `--validar` | flag | off | Corre validación del conjunto y termina. |
| `--solo_verificar` | flag | off | Corre equivalencia de lotes y termina. |
| `--trayectorias` | flag | off | Genera gráfico de trayectorias 3D. |

---

## Qué produce cada corrida

### Salida en consola (corrida normal)

    ============================================================
    Réplicas: 100 | pasos: 1000000 | dimensión: 3D
    Media x: ... (teórica 0)
    Media y: ... (teórica 0)
    Media z: ... (teórica 0)
    Desv. x: ... (teórica 1000.00)
    Desv. y: ... (teórica 1000.00)
    Desv. z: ... (teórica 1000.00)
    Retorno al origen DESPUÉS del paso 1000: ...
    ============================================================
    Tiempo: ... s

### Archivos generados

| Archivo | Cuándo | Contiene |
|---|---|---|
| `<salida>/scatter_3d.png` | Siempre | Scatter 3D de posiciones finales. |
| `<salida>/proyecciones_3d.png` | Siempre | Proyecciones ortogonales xy, xz, yz. |
| `<salida>/trayectorias_3d.png` | Con `--trayectorias` | 5 trayectorias en 3D. |
| `<salida>/finales_3d.csv` | Siempre | réplica, semilla, x, y, z, visito_despues. |

---

## Descripción del algoritmo

### Idea general

La rana parte del origen (0, 0, 0). En cada paso elige una de 6
direcciones con probabilidad 1/6 cada una:

- ±x
- ±y
- ±z

La decisión se hace con **un solo uniforme `R ∈ [0, 1)`** por paso:

- `R < 1/6` → (+1, 0, 0)
- `1/6 ≤ R < 2/6` → (−1, 0, 0)
- `2/6 ≤ R < 3/6` → (0, +1, 0)
- `3/6 ≤ R < 4/6` → (0, −1, 0)
- `4/6 ≤ R < 5/6` → (0, 0, +1)
- `5/6 ≤ R < 1`