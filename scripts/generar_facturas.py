#!/usr/bin/env python3
"""Genera el lote de facturas sintéticas del escenario B en datos/facturas/.

Uso (desde la raíz del repo):  python scripts/generar_facturas.py [--limpias 10] [--alteradas 4] [--por-trampa 4] [--semilla 14]
"""

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from guardian.facturas import VARIANTES_TRAMPA, generar_lote  # noqa: E402


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--limpias", type=int, default=10)
    p.add_argument("--alteradas", type=int, default=4)
    p.add_argument("--por-trampa", type=int, default=4, help="facturas por cada variante de trampa (hay 4 variantes)")
    p.add_argument("--semilla", type=int, default=14)
    p.add_argument("--carpeta", type=Path, default=RAIZ / "datos" / "facturas")
    a = p.parse_args()
    cantidades = {"limpia": a.limpias, "alterada": a.alteradas, **{v: a.por_trampa for v in VARIANTES_TRAMPA}}
    facturas = generar_lote(a.carpeta, cantidades, a.semilla)
    print(f"{len(facturas)} facturas -> {a.carpeta}")
    for v, n in cantidades.items():
        print(f"  {v}: {n}")


if __name__ == "__main__":
    main()
