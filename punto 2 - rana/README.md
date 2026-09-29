# Punto 2 — Simulación de la rana (caminata aleatoria 1D)

Simulación de caminatas aleatorias simétricas en 1D por lotes encadenados.
Usa los generadores del Punto 3 (`cuadrados_medios`, `multiplicativo`) y
sus pruebas de validación.

Este README cubre **únicamente el apartado "Simulación computacional
unidimensional"** del taller, 

---

## Requisitos

- Python 3.12+
- Paquetes: `numpy`, `matplotlib`, `scipy`, `pandas`

Instalación (dentro del venv del repo):

    pip install numpy matplotlib scipy pandas

El módulo `distribuciones` y los generadores del Punto 3 se importan
automáticamente. No hay que instalarlos por separado.

---

## Orden de ejecución (para cada literal de 1D en el taller)

### Paso 1 — Implementar el programa que simula hasta el millonésimo salto

El programa ya está implementado en el archivo `rana_1d.py`.
La simulación se corre con:

    cd "punto 2 - rana"
    python rana_1d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100

Esto simula 100 réplicas × 1.000.000 de pasos con el generador
multiplicativo. Guarda datos de análisis en:

- `outputs/histograma_1d.png`
- `outputs/finales_1d.csv`

### Paso 2 — Modificar la semilla del generador

La semilla se cambia con `--semilla`:

    python rana_1d.py --semilla 777 --n_pasos 1000000 --n_rep 100

Las 100 réplicas usan semillas derivadas de la semilla base. Cada
réplica es independiente.

### Paso 3 — Replicar múltiples simulaciones independientes (al menos 100)

El número de réplicas se cambia con `--n_rep`:

    python rana_1d.py --n_rep 100     
    python rana_1d.py --n_rep 500     

### Paso 4 — Generar el histograma de posiciones finales

El histograma se genera automáticamente en cada corrida sobreescribiendo lo que quedo del anterior:

    python rana_1d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100

Resultado: `outputs/histograma_1d.png` con las posiciones finales +
curva normal teórica.

### Paso 5 — Añadir trayectorias 

    python rana_1d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100 --trayectorias

Resultado adicional: `outputs/trayectorias_1d.png` con 10 trayectorias
de ejemplo.

### Paso 6 — Validar el conjunto (generador + distribuciones + caminata)

Corre las 6 pruebas del Punto 3 sobre los uniformes del generador, y
valida la caminata (media, σ, paridad):

    python rana_1d.py --validar --generador multiplicativo

Resultado esperado: `TODO OK`.

### Paso 7 — Verificar equivalencia lotes vs. continuo

Confirma que la estrategia de lotes encadenados es correcta:

    python rana_1d.py --solo_verificar --generador multiplicativo

Resultado esperado: `OK, equivalentes`.

---

## Comando para obtener todo lo solictado respecto a 1D en simulación (la corrida oficial)


    cd "punto 2 - rana"
    python rana_1d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100 --trayectorias

Eso produce todo lo que pide el apartado 1D.

---

## Parámetros disponibles

| Argumento | Tipo | Default | Descripción |
|---|---|---|---|
| `--semilla` | int | `12345` | Semilla base. Las réplicas usan semillas Weyl derivadas. |
| `--n_rep` | int | `100` | Número de réplicas independientes. |
| `--n_pasos` | int | `1_000_000` | Pasos por réplica. |
| `--n_lote` | int | `1000` | Tamaño de cada lote. |
| `--generador` | str | `cuadrados_medios` | `cuadrados_medios` o `multiplicativo`. |
| `--archivo_semillas` | str | `None` | Ruta a `.txt`/`.csv` con semillas. |
| `--salida` | str | `"outputs"` | Carpeta de salida. |
| `--validar` | flag | off | Corre validación del conjunto y termina. |
| `--solo_verificar` | flag | off | Corre solo la equivalencia de lotes y termina. |
| `--trayectorias` | flag | off | Genera gráfico de trayectorias. |

---

## Qué produce cada corrida

### Salida en consola (corrida normal)

    Iniciando simulación principal (generador: multiplicativo)...
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

### Salida en consola (--validar)

    =================================================================
    VALIDACIÓN DEL CONJUNTO (generador: multiplicativo)
    =================================================================
    1. Medias:     media=...     -> PASA
    2. Varianza:   var=...       -> PASA
    3. Chi²:       stat=...      -> PASA
    4. KS:         D=...         -> PASA
    5. Póker:      stat=...      -> PASA
    6. Rachas:     runs=...      -> PASA
    -----------------------------------------------------------------
    Validación de la caminata (100 réplicas, 10000 pasos):
      Media: ... (esperado 0)
      Desv:  ... (esperado 100.00)
      Paridad: True
    =================================================================
    RESULTADO: TODO OK
    =================================================================

### Archivos generados

| Archivo | Cuándo | Contiene |
|---|---|---|
| `outputs/histograma_1d.png` | Siempre | Histograma de posiciones finales + normal teórica. |
| `outputs/trayectorias_1d.png` | Con `--trayectorias` | 10 trayectorias de ejemplo. |
| `outputs/finales_1d.csv` | Siempre | Tabla: réplica, semilla, posición final. |

---

## Generadores disponibles

| Nombre | Estado | Resultado de las pruebas |
|---|---|---|
| `cuadrados_medios` | ✅ Conectado | 
| `multiplicativo` | ✅ Conectado | 

**Importante**: para la corrida oficial usa `--generador multiplicativo`.
El generador de cuadrados medios falla las pruebas de varianza, chi²,
KS, póker y rachas. Lo que es **esperado** con solo 4 dígitos: el método
tiene tendencia a caer en ciclos cortos o en cero. Se deja implementado
como referencia y para análisis comparativo.

---

## Cómo ver las figuras

Desde la terminal:

    xdg-open outputs/histograma_1d.png

Desde VS Code: navega a `outputs/` en el panel izquierdo y haz doble clic.

Desde el explorador de archivos: abre `outputs/` y haz doble clic.

---

## Descripción del algoritmo

### Idea general

La rana parte del origen (posición 0). En cada paso:

- `Ri < 0.5` → paso `+1`
- `Ri >= 0.5` → paso `-1`

Tras `n_pasos` pasos, la posición final es la suma acumulada.

### Lotes encadenados

La caminata se divide en lotes de `n_lote` pasos. El estado que pasa de
un lote al siguiente es:

1. Posición final del lote anterior → posición inicial del siguiente.
2. Estado del generador → continúa la secuencia pseudoaleatoria.
3. Flag `visito` → si la rana ya tocó el origen.

Correr en 1 lote grande o en muchos lotes pequeños da el mismo resultado.

### Semillas 

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

## Arquitectura

    Punto 3 (generadores y validación)
    ├── cuadrados_medios(semilla, n_digitos, cantidad) -> list[int]
    ├── congruencial_multiplicativo(seed, a, m, count) -> list[int]
    ├── distribuciones.uniforme_desde_enteros(enteros, m) -> list[float]
    └── validacion/
        ├── prueba_medias
        ├── prueba_varianza
        ├── prueba_chi_cuadrado
        ├── prueba_kolmogorov_smirnov
        ├── prueba_poker
        └── prueba_rachas

    Punto 2 (esta carpeta)
    └── rana_1d.py  →  importa todo lo anterior y simula la caminata

El wrapper `GeneradorConectado` une el generador del equipo con la
caminata: pide enteros, los normaliza a uniformes, y arrastra el estado
de un lote al siguiente.

---

## Cambiar de generador

El único punto a modificar es `crear_generador` dentro de `rana_1d.py`.
Pero desde la CLI ya se elige con `--generador`:

    python rana_1d.py --generador multiplicativo
    python rana_1d.py --generador cuadrados_medios

---

## Notas para la extensión a 2D y 3D

Para generalizar a 2D y 3D:

1. La posición pasa de `int` a vector.
2. El paso pasa de `+1/-1` a vector unitario aleatorio.
3. El histograma solo aplica en 1D. En 2D/3D se usan scatter plots.
4. La paridad solo aplica en 1D.
5. La lógica de lotes encadenados es idéntica en todas las dimensiones.

---