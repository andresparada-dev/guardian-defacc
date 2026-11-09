#!/usr/bin/env python3
"""Revisa que el computador esté listo para el sábado. No gasta créditos salvo con --probar-api.

Uso (desde la raíz del repo):  python verificar_entorno.py [--probar-api gemini|openai]
"""

import argparse
import importlib
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))


def revisar(nombre, ok, detalle="", opcional=False):
    marca = "OK" if ok else ("--" if opcional else "!!")
    print(f"[{marca}] {nombre}{(' · ' + detalle) if detalle else ''}")
    return ok


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--probar-api", choices=["gemini", "openai"], help="hace UNA llamada real de prueba")
    a = p.parse_args()
    todo = revisar("Python 3.11 o superior", sys.version_info >= (3, 11), sys.version.split()[0])
    for modulo, para in [("pydantic", "esquemas"), ("PIL", "facturas"), ("pandas", "análisis"), ("matplotlib", "gráficos"),
                         ("pytest", "pruebas")]:
        try:
            importlib.import_module(modulo)
            todo &= revisar(f"{modulo} ({para})", True)
        except ImportError:
            todo &= revisar(f"{modulo} ({para})", False, "pip install -r requirements.txt")
    for modulo, para in [("google.genai", "Gemini"), ("openai", "OpenAI de respaldo"), ("pytesseract", "OCR")]:
        try:
            importlib.import_module(modulo)
            revisar(f"{modulo} ({para})", True)
        except ImportError:
            revisar(f"{modulo} ({para}, opcional)", False, "pip install -r requirements.txt", opcional=True)
    from guardian.ocr import ocr_disponible
    revisar("Tesseract instalado (OCR, opcional)", ocr_disponible(), "en Colab: apt-get install -y tesseract-ocr tesseract-ocr-spa", opcional=True)
    revisar("Clave de Gemini (necesaria el sábado)", bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")), "variable GEMINI_API_KEY", opcional=True)
    revisar("Clave de OpenAI (respaldo)", bool(os.environ.get("OPENAI_API_KEY")), "variable OPENAI_API_KEY", opcional=True)
    todo &= revisar("Tabla de cifras oficiales", (RAIZ / "datos" / "hechos_oficiales.csv").exists())
    todo &= revisar("Base de conocimiento", (RAIZ / "datos" / "base_conocimiento.txt").exists())
    todo &= revisar("Casos del escenario A", (RAIZ / "datos" / "casos_cifras.json").exists())
    revisar("Facturas generadas", (RAIZ / "datos" / "facturas" / "indice.json").exists(), "python scripts/generar_facturas.py", opcional=True)
    if a.probar_api:
        from guardian.llm import crear_modelo
        try:
            r = crear_modelo(a.probar_api).generar_json('Responde SOLO JSON: {"ok": true}', "Prueba de conexión. Devuelve el JSON.")
            revisar(f"Llamada real a {a.probar_api}", bool(r.get("ok")), str(r))
        except Exception as e:
            revisar(f"Llamada real a {a.probar_api}", False, f"{type(e).__name__}: {e}")
    print("\nLo obligatorio está listo. Lo marcado con -- es opcional o se consigue antes del sábado." if todo
          else "\nHay pendientes obligatorios (marcados con !!).")


if __name__ == "__main__":
    main()
