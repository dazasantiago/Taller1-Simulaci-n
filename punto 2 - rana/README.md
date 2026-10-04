# Punto 2 — Simulación de la rana (caminata aleatoria 1D)

Simulación de caminatas aleatorias simétricas en 1D por lotes encadenados.
Usa los generadores del Punto 3 (`cuadrados_medios`, `lineal`,
`multiplicativo`) y las pruebas de validación.

Este README cubre **únicamente el apartado "Simulación computacional
unidimensional"** del taller, en el orden en que lo pide el enunciado.

---

## Requisitos

- Python 3.12+
- Paquetes: `numpy`, `matplotlib`, `scipy`, `pandas`

Instalación (dentro del venv del repo):

    pip install numpy matplotlib scipy pandas

El módulo `distribuciones` y los generadores del Punto 3 se importan
automáticamente. No hay que instalarlos por separado.

---

## Ejecución y parámetros

### Implementar el programa que simula hasta el millonésimo salto

cd "punto 2 - rana" (estar en la carpeta del punto 2)

Se ejecuta este literal del taller con el comando:

    
    python rana_1d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100

Esto simula 100 réplicas cada una de 1.000.000 de pasos con el generador
multiplicativo. Guarda:

- `outputs/histograma_1d.png`
- `outputs/finales_1d.csv`

### Modificar la semilla del generador

La semilla se cambia con `--semilla`:

    python rana_1d.py --semilla 777 --n_pasos 1000000 --n_rep 100

Las 100 réplicas usan semillas derivadas de la semilla base. Cada
réplica es independiente.

### Replicar múltiples simulaciones independientes (mínimo)

El número de réplicas se cambia con `--n_rep`:

    python rana_1d.py --n_rep 100     # mínimo del taller
    python rana_1d.py --n_rep 500     # más réplicas para histograma suave

### Para generar el histograma de posiciones finales de las replicas

El histograma se genera automáticamente en cada corrida:

    python rana_1d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100

Resultado: `outputs/histograma_1d.png` con las posiciones finales +
curva normal teórica.

### Visualización de trayectorias (trazas de simulación) 

La trayectoria para la simulación se obtiene añadiendo el parámetro

    python rana_1d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100 --trayectorias

Resultado adicional: `outputs/trayectorias_1d.png` con 10 trayectorias
de ejemplo.

### Validación el conjunto (generador + distribuciones + caminata)

Corre las 6 pruebas del Punto 3 sobre los uniformes del generador, y
valida la caminata (media, σ, paridad):

    python rana_1d.py --validar --generador multiplicativo

Resultado esperado: `TODO OK`.

---
## Comando de ejecución completo para 1D

Para ejecutar lo solicitado por el apartado de 1D :
- Implementen un programa que simule el comportamiento de la rana hasta el millonésimo salto en una dimensión.

- El programa debe permitir modificar la semilla del generador aleatorio y replicar múltiples simulaciones independientes (al menos 100).

    cd "punto 2 - rana"
    python rana_1d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100 --trayectorias

Eso produce todo lo que pide el apartado 1D.

---

## Parámetros disponibles

| Argumento | Tipo | Default | Descripción |
|---|---|---|---|
| `--semilla` | int | `12345` | Semilla base. Las réplicas usan semillas derivadas. |
| `--n_rep` | int | `100` | Número de réplicas independientes. |
| `--n_pasos` | int | `1_000_000` | Pasos por réplica. |
| `--n_lote` | int | `1000` | Tamaño de cada lote. |
| `--generador` | str | `cuadrados_medios` | `cuadrados_medios`, `lineal` o `multiplicativo`. |
| `--archivo_semillas` | str | `None` | Ruta a `.txt`/`.csv` con semillas. |
| `--salida` | str | `"outputs"` | Carpeta de salida de PNG y CSV. |
| `--validar` | flag | off | Corre validación del conjunto y termina. |
| `--solo_verificar` | flag | off | Corre solo la equivalencia de lotes y termina. |
| `--trayectorias` | flag | off | Genera gráfico de trayectorias. |

---

## Generadores disponibles

| Nombre | Estado | ¿Pasa las 6 pruebas? | Firma |
|---|---|---|---|
| `cuadrados_medios` | Conectado | `(semilla, n_digitos, cantidad)` |
| `lineal` | Conectado | Pasa las 6 pruebas | `(seed, a, c, m, count)` |
| `multiplicativo` | Conectado | Pasa las 6 pruebas | `(seed, a, m, count)` |

**Recomendación**: usa `multiplicativo` para la corrida oficial. `lineal`
también funciona pero el multiplicativo suele dar mejores resultados
en las pruebas.

`cuadrados_medios` se deja implementado como referencia y para análisis
comparativo. Falla porque con solo 4 dígitos tiende a caer en ciclos
cortos o en cero. Esto es un resultado válido y didáctico.

---

## Ejecutar con cada generador

Para comparar los tres generadores sin sobrescribir figuras:

    python rana_1d.py --generador multiplicativo --n_pasos 1000000 --n_rep 100 --salida outputs/multiplicativo
    python rana_1d.py --generador lineal --n_pasos 1000000 --n_rep 100 --salida outputs/lineal
    python rana_1d.py --generador cuadrados_medios --n_pasos 1000000 --n_rep 100 --salida outputs/cuadrados_medios

Cada corrida deja sus PNGs y CSV en su propia carpeta.

Validar los tres:

    python rana_1d.py --validar --generador multiplicativo
    python rana_1d.py --validar --generador lineal
    python rana_1d.py --validar --generador cuadrados_medios

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
| `<salida>/histograma_1d.png` | Siempre | Histograma de posiciones finales + normal teórica. |
| `<salida>/trayectorias_1d.png` | Con `--trayectorias` | 10 trayectorias de ejemplo. |
| `<salida>/finales_1d.csv` | Siempre | Tabla: réplica, semilla, posición final. |

Donde `<salida>` es el valor de `--salida` (default: `outputs`).

---

## Cómo ver las figuras

Desde la terminal:

    xdg-open outputs/histograma_1d.png

Desde VS Code: navega a la carpeta de salida en el panel izquierdo y
haz doble clic en el PNG.

Desde el explorador de archivos: abre la carpeta y haz doble clic.

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

Si usas `--salida outputs/<nombre>`, se crea una subcarpeta por corrida.

---

## Arquitectura

    Punto 3 (generadores y validación)
    ├── cuadrados_medios(semilla, n_digitos, cantidad) -> list[int]
    ├── congruencial_lineal(seed, a, c, m, count) -> list[int]
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
de un lote al siguiente. Se adapta a los nombres de los parámetros de
cada generador (`cantidad`/`count`, `semilla`/`seed`).

---

## Cambiar de generador

Se elige desde la CLI con `--generador`:

    python rana_1d.py --generador multiplicativo
    python rana_1d.py --generador lineal
    python rana_1d.py --generador cuadrados_medios

Si quieres añadir otro generador en el futuro, el único punto a
modificar es `crear_generador` dentro de `rana_1d.py`.

---

