"""Punto de entrada de línea de comandos del módulo.

Permite (una vez implementada la lógica):
    - Leer semillas/parámetros desde un archivo (.txt/.csv) o ingresarlos
      manualmente por consola.
    - Seleccionar uno o varios métodos de generación de números
      pseudoaleatorios.
    - Seleccionar una o varias pruebas de validación estadística a
      ejecutar sobre la secuencia generada (o leída).

Este archivo SOLO define el esqueleto de argumentos (`argparse`) y del
menú interactivo. NO contiene lógica real de generación ni de
validación: las funciones de despacho (`comando_generar`,
`comando_validar`) deben delegar en `src.generadores` y
`src.validacion` cuando el equipo las implemente.

Uso previsto (una vez implementado):
    python main.py generar --metodo congruencial_lineal --semilla 7 \
        --a 1093 --c 18257 --m 86436 --cantidad 100 --salida datos.csv

    python main.py validar --entrada datos.csv --prueba chi_cuadrado ks

    python main.py            # sin argumentos -> abre el menú interactivo
"""

from __future__ import annotations

import argparse
from pathlib import Path

METODOS_GENERACION = (
    "cuadrados_medios",
    "congruencial_lineal",
    "congruencial_multiplicativo",
    "congruencial_aditivo",
    "uniforme",
    "normal",
)
"""Métodos de generación seleccionables desde la CLI/menú."""

PRUEBAS_VALIDACION = (
    "medias",
    "varianza",
    "chi_cuadrado",
    "ks",
    "poker",
    "rachas",
)
"""Pruebas de validación seleccionables desde la CLI/menú."""


def leer_semillas_archivo(ruta: str | Path) -> list[float]:
    """Lee una lista de semillas/números desde un archivo `.txt` o `.csv`.

    Args:
        ruta: Ruta al archivo de entrada. Se espera soportar al menos:
            - `.txt`: un valor por línea (líneas que empiecen con `#`
              se consideran comentarios y deben ignorarse).
            - `.csv`: con una columna identificable (ej. "semilla") u
              otra convención que el equipo defina y documente en
              `docs/README.md`.

    Returns:
        list[float]: Lista de valores leídos desde el archivo, en el
        orden en que aparecen.

    Raises:
        NotImplementedError: Función pendiente de implementación.
        FileNotFoundError: (a implementar) si `ruta` no existe.

    TODO:
        - Detectar la extensión del archivo y despachar al parser
          correspondiente (txt vs csv).
        - Ignorar líneas vacías y comentarios (`#`) en el caso `.txt`.
        - Usar `pandas` para leer el `.csv` de forma robusta.
    """
    # TODO: Implementar la lectura de semillas desde archivo.
    raise NotImplementedError("leer_semillas_archivo: pendiente de implementación")


def leer_semillas_manual() -> list[float]:
    """Solicita semillas/números al usuario por consola, uno o varios por línea.

    Returns:
        list[float]: Lista de valores ingresados por el usuario.

    Raises:
        NotImplementedError: Función pendiente de implementación.

    TODO:
        - Definir el formato de entrada esperado (ej. valores separados
          por espacios o comas, finalizar con línea vacía).
        - Validar que los valores ingresados sean numéricos.
    """
    # TODO: Implementar la lectura manual de semillas.
    raise NotImplementedError("leer_semillas_manual: pendiente de implementación")


def construir_parser() -> argparse.ArgumentParser:
    """Construye el `ArgumentParser` de la CLI con sus subcomandos.

    Subcomandos:
        - `generar`: genera una secuencia de números pseudoaleatorios.
        - `validar`: ejecuta una o varias pruebas de validación sobre
          una secuencia (leída desde archivo).

    Returns:
        argparse.ArgumentParser: Parser configurado con los subcomandos
        y sus argumentos (sin lógica de ejecución asociada).
    """
    parser = argparse.ArgumentParser(
        prog="main.py",
        description=(
            "Biblioteca de generación y validación de números "
            "pseudoaleatorios (Taller 1 - Simulación)."
        ),
    )
    subparsers = parser.add_subparsers(dest="comando")

    # --- Subcomando: generar ---
    generar_parser = subparsers.add_parser(
        "generar", help="Genera una secuencia de números pseudoaleatorios."
    )
    generar_parser.add_argument(
        "--metodo", choices=METODOS_GENERACION, required=True,
        help="Método de generación a utilizar.",
    )
    generar_parser.add_argument(
        "--semilla-archivo", type=str, default=None,
        help="Ruta a un archivo .txt/.csv con semilla(s) de entrada.",
    )
    generar_parser.add_argument(
        "--semilla", type=float, nargs="*", default=None,
        help="Semilla(s) ingresadas directamente por línea de comandos.",
    )
    generar_parser.add_argument(
        "--cantidad", type=int, required=True,
        help="Cantidad de números a generar.",
    )
    generar_parser.add_argument(
        "--n-digitos", type=int, default=None,
        help="Cantidad de dígitos (requerido por Cuadrados Medios).",
    )
    generar_parser.add_argument(
        "--a", type=float, default=None, help="Parámetro 'a' (métodos congruenciales).",
    )
    generar_parser.add_argument(
        "--c", type=float, default=None, help="Parámetro 'c' (Congruencial Lineal).",
    )
    generar_parser.add_argument(
        "--m", type=float, default=None, help="Módulo 'm' (métodos congruenciales).",
    )
    generar_parser.add_argument(
        "--salida", type=str, default=None,
        help="Ruta de archivo (csv) donde exportar la secuencia generada.",
    )

    # --- Subcomando: validar ---
    validar_parser = subparsers.add_parser(
        "validar", help="Ejecuta pruebas de validación estadística sobre una secuencia."
    )
    validar_parser.add_argument(
        "--entrada", type=str, required=True,
        help="Archivo (txt/csv) con la secuencia a validar.",
    )
    validar_parser.add_argument(
        "--prueba", choices=PRUEBAS_VALIDACION, nargs="+", required=True,
        help="Una o varias pruebas de validación a ejecutar.",
    )
    validar_parser.add_argument(
        "--nivel-confianza", type=float, default=0.95,
        help="Nivel de confianza para pruebas de medias/varianza (default 0.95).",
    )
    validar_parser.add_argument(
        "--n-intervalos", type=int, default=None,
        help="Cantidad de intervalos para la prueba Chi-cuadrado.",
    )
    validar_parser.add_argument(
        "--tam-mano", type=int, default=5,
        help="Tamaño de mano (dígitos) para la prueba de Póker (default 5).",
    )

    return parser


def comando_generar(args: argparse.Namespace) -> None:
    """Despacha la ejecución del subcomando `generar`.

    Args:
        args: Argumentos parseados por `construir_parser()`.

    Raises:
        NotImplementedError: Función pendiente de implementación.

    TODO:
        - Resolver las semillas/parámetros desde `--semilla-archivo` o
          `--semilla` (o lanzar error si no se provee ninguno).
        - Llamar a la función de `src.generadores` correspondiente a
          `args.metodo` con los parámetros armados.
        - Si `args.salida` está definido, exportar la secuencia
          resultante (ej. con `pandas`) a esa ruta.
        - Si no, imprimir o mostrar un resumen de la secuencia generada.
    """
    # TODO: Implementar el despacho del subcomando 'generar'.
    raise NotImplementedError("comando_generar: pendiente de implementación")


def comando_validar(args: argparse.Namespace) -> None:
    """Despacha la ejecución del subcomando `validar`.

    Args:
        args: Argumentos parseados por `construir_parser()`.

    Raises:
        NotImplementedError: Función pendiente de implementación.

    TODO:
        - Leer la secuencia desde `args.entrada` (ver `leer_semillas_archivo`).
        - Por cada prueba en `args.prueba`, llamar a la función
          correspondiente de `src.validacion.pruebas_estadisticas`.
        - Mostrar/guardar los resultados y las figuras generadas
          (ej. en `outputs/`).
    """
    # TODO: Implementar el despacho del subcomando 'validar'.
    raise NotImplementedError("comando_validar: pendiente de implementación")


def menu_interactivo() -> None:
    """Menú interactivo por consola (alternativa a los argumentos de CLI).

    Estructura esperada del menú (a implementar):
        1. Leer semillas (desde archivo o ingreso manual).
        2. Seleccionar método(s) de generación.
        3. Seleccionar prueba(s) de validación a ejecutar.
        4. Ejecutar y mostrar/guardar resultados.
        5. Salir.

    Raises:
        NotImplementedError: Función pendiente de implementación.

    TODO:
        - Implementar el ciclo de menú (mostrar opciones, leer elección).
        - Conectar cada opción con `leer_semillas_archivo`,
          `leer_semillas_manual`, `comando_generar` y `comando_validar`.
    """
    opciones = (
        "1. Leer semillas desde archivo",
        "2. Ingresar semillas manualmente",
        "3. Seleccionar método(s) de generación",
        "4. Seleccionar prueba(s) de validación",
        "5. Ejecutar",
        "6. Salir",
    )
    for opcion in opciones:
        print(opcion)
    # TODO: Implementar el ciclo de lectura de opción y despacho real.
    raise NotImplementedError("menu_interactivo: pendiente de implementación")


def main() -> None:
    """Punto de entrada principal del script.

    Si se invoca sin argumentos, debería abrir el menú interactivo
    (`menu_interactivo`); si se invoca con un subcomando (`generar` /
    `validar`), debería despachar a la función correspondiente.

    TODO:
        - Decidir el comportamiento exacto sin argumentos (menú) vs.
          con subcomando (CLI no interactiva) y conectarlo aquí.
    """
    parser = construir_parser()
    args = parser.parse_args()

    if args.comando == "generar":
        comando_generar(args)
    elif args.comando == "validar":
        comando_validar(args)
    else:
        menu_interactivo()


if __name__ == "__main__":
    main()
