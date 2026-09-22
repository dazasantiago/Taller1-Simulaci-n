"""Lectura de semillas desde texto manual o archivos .txt / .csv.

Solo hace entrada/salida y validación de formato; no genera números.
"""

from __future__ import annotations

import csv
import io
import re


def _a_entero(token: str) -> int:
    """Convierte un token a entero no negativo (acepta '5735' y '5735.0')."""
    token = token.strip()
    try:
        valor = int(token)
    except ValueError:
        try:
            decimal = float(token)
        except ValueError:
            raise ValueError(f"'{token}' no es un entero válido") from None
        if not decimal.is_integer():
            raise ValueError(f"'{token}' no es un entero válido") from None
        valor = int(decimal)
    if valor < 0:
        raise ValueError(f"la semilla {valor} es negativa; deben ser enteros no negativos")
    return valor


def parsear_texto(texto: str) -> list[int]:
    """Semillas separadas por comas, punto y coma, espacios o saltos de línea.

    Ignora líneas vacías y todo lo que siga a un '#' (comentarios).
    """
    semillas: list[int] = []
    for linea in texto.splitlines():
        linea = linea.split("#", 1)[0]
        for token in re.split(r"[,;\s]+", linea):
            if token:
                semillas.append(_a_entero(token))
    return semillas


def _es_numero(token: str) -> bool:
    try:
        float(token)
    except ValueError:
        return False
    return True


def _leer_csv(texto: str) -> list[int]:
    filas = [
        fila
        for fila in csv.reader(io.StringIO(texto))
        if fila and not fila[0].lstrip().startswith("#")
    ]
    if not filas:
        return []

    # Con encabezado (alguna celda no numérica) se busca la columna 'semilla';
    # sin encabezado se toma la primera columna.
    columna = 0
    if not all(_es_numero(c) for c in filas[0] if c.strip()):
        encabezado = [c.strip().lower() for c in filas[0]]
        for nombre in ("semilla", "semillas"):
            if nombre in encabezado:
                columna = encabezado.index(nombre)
                break
        filas = filas[1:]

    return [_a_entero(fila[columna]) for fila in filas if len(fila) > columna and fila[columna].strip()]


def leer_archivo(nombre: str, contenido: bytes) -> list[int]:
    """Lee las semillas de un archivo subido. Lanza ValueError si el formato es inválido."""
    texto = contenido.decode("utf-8-sig")
    if nombre.lower().endswith(".csv"):
        semillas = _leer_csv(texto)
    else:
        semillas = parsear_texto(texto)
    if not semillas:
        raise ValueError("el archivo no contiene semillas")
    return semillas
