"""Dígito de verificación del NIT colombiano (algoritmo módulo 11 de la DIAN).

Cada dígito del NIT, leído de derecha a izquierda, se multiplica por un peso fijo
(3, 7, 13, 17, 19, ...). Se suma todo y se toma el residuo al dividir por 11:
si el residuo es 0 o 1, ese es el dígito; si no, el dígito es 11 menos el residuo.
"""

import re

_PESOS = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]


def digito_verificacion(nit: str) -> int:
    digitos = re.sub(r"\D", "", nit)
    if not digitos or len(digitos) > len(_PESOS):
        raise ValueError(f"NIT inválido: {nit!r}")
    suma = sum(int(d) * p for d, p in zip(reversed(digitos), _PESOS))
    residuo = suma % 11
    return residuo if residuo in (0, 1) else 11 - residuo


def nit_valido(nit_con_dv: str) -> bool:
    """'900123456-8' -> True si el último dígito es el de verificación correcto."""
    m = re.fullmatch(r"\s*([\d.]+)\s*-\s*(\d)\s*", nit_con_dv or "")
    if not m:
        return False
    return digito_verificacion(m.group(1)) == int(m.group(2))
