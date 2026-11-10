#!/usr/bin/env python3
"""Corre la medición y deja los resultados en resultados/<fecha>_<modelo>/.

Ejemplos (desde la raíz del repo):
  python scripts/medir.py --modelo comprometido --ocr simulado          # prueba sin internet (peor caso)

  # Plan gratuito de Gemini (unas 20 llamadas al día): 8 casos de A + 12 facturas = 20 llamadas
  python scripts/medir.py --modelo gemini --preset minimo --n-ataques 5 --n-legitimas 3 --n-facturas 12 --max-llamadas 20

  python scripts/medir.py --modelo gemini --preset completo             # medición completa (si hay cuota)
  python scripts/medir.py --modelo gemini --casos A01,A02,L01 --escenarios A

Presets: minimo (1 llamada por caso), medio (2) y completo (3, más una o dos por cada ataque que la
capa de firmas mande a cuarentena). La compuerta y las firmas no gastan llamadas.
Si se acaba la cuota, corre el mismo comando otro día: lo ya respondido sale de la caché.
"""

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from guardian import escenario_cifras as A  # noqa: E402
from guardian.facturas import cargar_lote  # noqa: E402
from guardian.hechos import TablaOficial  # noqa: E402
from guardian.llm import crear_modelo  # noqa: E402
from guardian.medidor import PRESETS, correr_todo, estimar_llamadas, seleccionar_casos, seleccionar_facturas  # noqa: E402
from guardian.ocr import ocr_disponible  # noqa: E402


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modelo", default="comprometido", help="comprometido | gemini | gemini:<versión> | openai | openai:<versión>")
    p.add_argument("--preset", default="completo", choices=sorted(PRESETS), help="qué configuraciones de defensa medir")
    p.add_argument("--ocr", default="real", choices=["real", "simulado", "no"],
                   help="real = Tesseract; simulado = texto impreso (solo para pruebas); no = sin segunda lectura")
    p.add_argument("--escenarios", default="A,B", help="A, B o A,B")
    p.add_argument("--n-ataques", type=int, help="usar solo los primeros N ataques del escenario A")
    p.add_argument("--n-legitimas", type=int, help="usar solo las primeras N preguntas legítimas del escenario A")
    p.add_argument("--casos", help="ids exactos del escenario A, separados por coma (por ejemplo A01,A04,L02)")
    p.add_argument("--n-facturas", type=int, help="usar N facturas, balanceadas entre variantes")
    p.add_argument("--max-llamadas", type=int, help="tope de llamadas reales en esta corrida (la caché no cuenta)")
    p.add_argument("--espera", type=float, default=None, help="segundos mínimos entre llamadas (por defecto 7 con modelos reales)")
    p.add_argument("--facturas", type=Path, default=RAIZ / "datos" / "facturas")
    a = p.parse_args()

    tabla = TablaOficial()
    espera = a.espera if a.espera is not None else (0 if a.modelo == "comprometido" else 7)
    modelo = crear_modelo(a.modelo, tabla, max_llamadas=a.max_llamadas, espera_min=espera)
    nombre = getattr(modelo, "nombre", a.modelo)
    escenarios = tuple(x.strip().upper() for x in a.escenarios.split(","))
    configuraciones = PRESETS[a.preset]

    casos_a = seleccionar_casos(A.cargar_casos(), a.n_ataques, a.n_legitimas, a.casos.split(",") if a.casos else None)
    carpeta = a.facturas if (a.facturas / "indice.json").exists() else None
    if "B" in escenarios and carpeta is None:
        print("No hay facturas: corre primero  python scripts/generar_facturas.py")
    n_a = len(casos_a["ataques"]) + len(casos_a["legitimas"]) if "A" in escenarios else 0
    n_b = len(seleccionar_facturas(cargar_lote(carpeta), a.n_facturas)) if ("B" in escenarios and carpeta) else 0

    print(f"Modelo: {nombre} · preset: {a.preset} · casos A: {n_a} · facturas: {n_b}")
    if a.modelo == "comprometido":
        print("Peor caso simulado: estos resultados miden la compuerta, no a la IA. No gasta llamadas.")
    else:
        maximo = estimar_llamadas(configuraciones, n_a, n_b, len(casos_a["ataques"]) if "A" in escenarios else 0)
        print(f"Esta corrida necesita hasta {maximo} llamadas (menos si ya hay respuestas en caché).")
        if a.max_llamadas is not None and maximo > a.max_llamadas:
            print(f"Ojo: el tope es {a.max_llamadas}. Se detendrá al llegar y podrás seguir otro día con el mismo comando.")
    if a.ocr == "real" and not ocr_disponible():
        print("Aviso: Tesseract no está instalado; la segunda lectura por OCR queda desactivada.")

    salida = correr_todo(modelo, nombre, carpeta, RAIZ / "resultados", a.ocr, escenarios, configuraciones, casos_a, a.n_facturas)
    print((salida / "resumen.md").read_text(encoding="utf-8"))
    print(f"Detalle, CSV y gráfico en: {salida}")


if __name__ == "__main__":
    main()
