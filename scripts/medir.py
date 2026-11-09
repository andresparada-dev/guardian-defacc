#!/usr/bin/env python3
"""Corre la medición completa y deja los resultados en resultados/<fecha>_<modelo>/.

Ejemplos (desde la raíz del repo):
  python scripts/medir.py --modelo comprometido --ocr simulado     # prueba sin internet (peor caso)
  python scripts/medir.py --modelo gemini                          # medición real (GEMINI_API_KEY)
  python scripts/medir.py --modelo openai --escenarios A           # solo cifras, con OpenAI
"""

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from guardian.hechos import TablaOficial  # noqa: E402
from guardian.llm import crear_modelo  # noqa: E402
from guardian.medidor import correr_todo  # noqa: E402
from guardian.ocr import ocr_disponible  # noqa: E402


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modelo", default="comprometido", help="comprometido | gemini | gemini:<versión> | openai | openai:<versión>")
    p.add_argument("--ocr", default="real", choices=["real", "simulado", "no"],
                   help="real = Tesseract; simulado = texto impreso (solo para pruebas); no = sin segunda lectura")
    p.add_argument("--escenarios", default="A,B", help="A, B o A,B")
    p.add_argument("--facturas", type=Path, default=RAIZ / "datos" / "facturas")
    a = p.parse_args()

    tabla = TablaOficial()
    modelo = crear_modelo(a.modelo, tabla)
    nombre = getattr(modelo, "nombre", a.modelo)
    if a.ocr == "real" and not ocr_disponible():
        print("Aviso: Tesseract no está instalado; la segunda lectura por OCR queda desactivada.")
    if a.modelo == "comprometido":
        print("Modelo comprometido (peor caso simulado): estos resultados miden la compuerta, no a la IA.")
    escenarios = tuple(x.strip().upper() for x in a.escenarios.split(","))
    carpeta = a.facturas if (a.facturas / "indice.json").exists() else None
    if "B" in escenarios and carpeta is None:
        print("No hay facturas: corre primero  python scripts/generar_facturas.py")
    salida = correr_todo(modelo, nombre, carpeta, RAIZ / "resultados", a.ocr, escenarios)
    print((salida / "resumen.md").read_text(encoding="utf-8"))
    print(f"Detalle, CSV y gráfico en: {salida}")


if __name__ == "__main__":
    main()
