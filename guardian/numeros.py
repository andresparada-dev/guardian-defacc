"""Lectura y escritura de números en formato colombiano.

En Colombia el punto separa miles y la coma separa decimales: 92.335 son noventa y dos mil
trescientos treinta y cinco; 47,2 % es cuarenta y siete coma dos por ciento. Los modelos de
lenguaje a veces responden en formato inglés (47.2 %), así que el lector acepta los dos.
"""

import re

# Un número con miles separados por punto (1.180.444), o con coma decimal (47,2), o en
# formato inglés (47.2). Se exige que no esté pegado a letras para no leer "SL5" como 5.
_PATRON = re.compile(r"(?<![\w.,])(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+\.\d+|\d+(?:,\d+)?)(?![\w]|[.,]\d)")


def leer_numero(token: str) -> float:
    """Convierte un número escrito en texto a float, aceptando formato colombiano e inglés."""
    t = token.strip()
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", t):  # 92.335 o 1.180,4
        return float(t.replace(".", "").replace(",", "."))
    if "," in t:  # 47,2
        return float(t.replace(",", "."))
    return float(t)  # 47.2 o 2023


def extraer_numeros(texto: str) -> list[float]:
    """Todos los números que aparecen en un texto, en el orden en que aparecen."""
    return [leer_numero(m.group(1)) for m in _PATRON.finditer(texto or "")]


def formatear(valor: float, decimales: int = 0) -> str:
    """Escribe un número en formato colombiano: 92335 -> '92.335', 47.17 -> '47,2' (1 decimal)."""
    texto = f"{valor:,.{decimales}f}"  # 92,335.00 en formato inglés
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def formatear_pesos(valor: int) -> str:
    """$ 4.250.000"""
    return "$ " + formatear(valor)
