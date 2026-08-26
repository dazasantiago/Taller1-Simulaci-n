# Interfaz gráfica (Streamlit) — en desarrollo

Esta carpeta contendrá la interfaz gráfica del proyecto, construida
con [Streamlit](https://streamlit.io/). Por ahora `app/main.py` es solo
un placeholder (título + comentarios TODO); la implementación real es
trabajo del equipo.

## Cómo correrla

Con el entorno virtual activado y las dependencias instaladas
(`pip install -r requirements.txt` desde la raíz del proyecto):

```bash
streamlit run app/main.py
```

Esto abre la app en el navegador (por defecto en `http://localhost:8501`).
Como hoy es un placeholder, solo debería verse el título de la página.

## Qué se espera que permita hacer la interfaz

Basado en los requisitos funcionales del taller, la interfaz debería
permitir, sin reimplementar la lógica (que vive en `src/`, ver
`docs/README.md` para el contrato de cada función):

- **Selección del método de generación**: elegir entre Cuadrados
  Medios, Congruencial Lineal, Congruencial Multiplicativo,
  Congruencial Aditivo, Uniforme o Normal, e ingresar los parámetros
  específicos de cada uno (semilla, `a`, `c`, `m`, `n_digitos`,
  semillas iniciales, cantidad de números a generar, etc.).
- **Carga de semillas**: desde un archivo `.txt`/`.csv` (ver
  `data/seeds/semillas_ejemplo.*` como referencia de formato) o
  ingresadas manualmente.
- **Selección de prueba(s) de validación**: elegir una o varias entre
  medias, varianza, chi-cuadrado, Kolmogorov-Smirnov (KS), póker y
  rachas, junto con sus parámetros específicos (nivel de confianza,
  número de intervalos, tamaño de mano).
- **Visualización de resultados**: mostrar la secuencia generada en
  una tabla, y por cada prueba ejecutada su estadístico, valor
  crítico/p-valor, la decisión (pasa/no pasa) y el gráfico
  correspondiente (histograma, CDF empírica vs. teórica, etc., según
  la prueba).

## Estado actual

- [x] Esqueleto mínimo de la app (`app/main.py`) y esta documentación.
- [ ] Selectores de método de generación y sus parámetros.
- [ ] Carga de semillas (archivo / manual).
- [ ] Selectores de prueba(s) de validación y sus parámetros.
- [ ] Ejecución y visualización de resultados (tablas y gráficos).

Ninguno de estos puntos pendientes debe implementarse hasta que las
funciones correspondientes en `src/generadores/` y `src/validacion/`
estén implementadas y probadas.
