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

## Estructura

- `main.py`: entrada; solo arma las dos pestañas (Generación / Validación).
- `tab_generacion.py`: un método a la vez, parámetros y semillas (manual o
  .txt/.csv), tabla exportable e histograma de cada secuencia.
- `tab_validacion.py`: secuencias en memoria agrupadas por método; botones
  para probar todas / un grupo / una secuencia y ver resultados.
- `catalogo.py`: único punto que toca `src/`. Solo ofrece los generadores y
  pruebas que ya están implementados; los placeholders no se muestran.
- `estado.py`: memoria de la sesión (`st.session_state`).
- `semillas.py`: lectura de semillas desde texto, .txt y .csv.

## Estado actual

- [x] Selector de método de generación, parámetros y semillas (archivo / manual).
- [x] Secuencias en memoria, tabla exportable e histograma.
- [x] Validación por secuencia, por grupo o de todas, con resultados por prueba.
- [ ] Probar con los generadores y pruebas reales cuando `src/` los tenga.
