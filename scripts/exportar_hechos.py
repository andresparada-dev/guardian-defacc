#!/usr/bin/env python3
"""Arma datos/hechos_oficiales.csv: la tabla de cifras oficiales que usa el guardián.

Fuente: las cifras verificadas del reto DANE (CENU 2024, módulo sectoral_reference_2023,
Bogotá D.C., resultados preliminares). Se leen del Excel verificado y del archivo de datos
del dashboard; unas pocas cifras derivadas vienen del análisis verificado del mismo reto.
También copia la base de conocimiento del agente a datos/base_conocimiento.txt.

La tabla ya viene generada en datos/. Solo hace falta correr esto si cambian las cifras del reto DANE.
Necesita una copia del repositorio DATATON-DANE-2026 (por defecto, al lado de este repositorio).

Uso (desde la raíz del repo):  python scripts/exportar_hechos.py [--repo-dane ../DATATON-DANE-2026]
"""

import argparse
import csv
import re
import shutil
from pathlib import Path

import openpyxl

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "datos" / "hechos_oficiales.csv"
EXCEL = DASHBOARD_JS = BASE_CONOCIMIENTO = None  # se definen en main() según --repo-dane


def _rutas(repo_dane: Path) -> None:
    global EXCEL, DASHBOARD_JS, BASE_CONOCIMIENTO
    EXCEL = repo_dane / "ruta2" / "entrega" / "ruta2_bogota_cifras_verificadas.xlsx"
    DASHBOARD_JS = repo_dane / "ruta2" / "insumos" / "dashboard_data_api.js"
    BASE_CONOCIMIENTO = repo_dane / "ruta2" / "entrega" / "agente_voz" / "base_conocimiento_ruta2_bogota.txt"

F_EXCEL = "Excel verificado del reto DANE (API del Visor CENU)"
F_ANALISIS = "Análisis verificado del reto DANE (base de conocimiento del agente)"

# Cifras derivadas que no están como celda en el Excel pero se verificaron en el reto DANE.
DERIVADAS = [
    ("comercio_pct", "% de las unidades de Bogotá en comercio (divisiones 45, 46 y 47)", 57.2, "%", 1),
    ("servicios_pct", "% de las unidades de Bogotá en servicios", 35.0, "%", 1),
    ("industria_pct", "% de las unidades de Bogotá en industria", 5.4, "%", 1),
    ("transporte_pct", "% de las unidades de Bogotá en transporte", 1.6, "%", 1),
    ("construccion_pct", "% de las unidades de Bogotá en construcción", 0.9, "%", 1),
    ("top10_pct", "% de las unidades de Bogotá en las 10 divisiones más grandes", 81.7, "%", 1),
    ("top3_pct", "% de las unidades de Bogotá en las 3 divisiones más grandes (47, 56 y 45)", 64.8, "%", 1),
    ("subsistencia_unidades", "Unidades en divisiones con señal de subsistencia (95, 96 y 47)", 106718, "unidades", 0),
    ("subsistencia_pct", "% de Bogotá en divisiones con señal de subsistencia (95, 96 y 47)", 54.5, "%", 1),
    ("div47_respuesta_ingreso_pct", "% de respuesta de la división 47 en ingreso", 71.5, "%", 1),
    ("div47_respuesta_personal_pct", "% de respuesta de la división 47 en personal ocupado", 69.4, "%", 1),
    ("bogota_ingreso_0a50_pct", "% de unidades de Bogotá que reportaron ingreso entre 0 y 50 millones", 49.8, "%", 1),
    ("nacional_ingreso_0a50_pct", "% de unidades del país que reportaron ingreso entre 0 y 50 millones", 61.2, "%", 1),
]


def _js_divisiones() -> dict[str, dict]:
    """Lee % con 1 a 5 personas y % con más de 50 personas por división desde el JS del dashboard."""
    texto = DASHBOARD_JS.read_text(encoding="utf-8")
    out = {}
    for obj in re.findall(r"\{(.*?)\}", texto, flags=re.S):
        div = re.search(r'division: "(\d+)"', obj)
        if div:
            num = lambda k: float(re.search(rf"\b{k}: ([\d.]+)", obj).group(1))
            out[div.group(1)] = {"lowPers": num("lowPers"), "highPers": num("highPers")}
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-dane", type=Path, default=RAIZ.parent / "DATATON-DANE-2026",
                   help="ruta a la copia local del repositorio DATATON-DANE-2026")
    _rutas(p.parse_args().repo_dane.resolve())
    wb = openpyxl.load_workbook(EXCEL, data_only=True)
    filas = []

    def agregar(clave, descripcion, valor, unidad, decimales, fuente=F_EXCEL):
        filas.append({"clave": clave, "descripcion": descripcion, "valor": valor,
                      "unidad": unidad, "decimales": decimales, "fuente": fuente})

    personas = _js_divisiones()
    ws = wb["top12_bogota"]
    cab = [c.value for c in ws[1]]
    for fila in ws.iter_rows(min_row=2, values_only=True):
        r = dict(zip(cab, fila))
        d, nombre = str(r["division"]), r["nombre"]
        agregar(f"div{d}_unidades", f"Unidades económicas de la división {d} ({nombre}) en Bogotá", r["unidades"], "unidades", 0)
        agregar(f"div{d}_pct_bogota", f"% de las unidades de Bogotá en la división {d} ({nombre})", r["pct_unidades_bogota"], "%", 1)
        agregar(f"div{d}_pct_ingreso_bajo", f"% de unidades de la división {d} ({nombre}) con ingreso 2023 de 0 a 10 millones", r["pct_bajo_ingreso"], "%", 1)
        agregar(f"div{d}_pct_ingreso_alto", f"% de unidades de la división {d} ({nombre}) con ingreso 2023 de más de 1.000 millones", r["pct_alto_ingreso"], "%", 1)
        if d in personas:
            agregar(f"div{d}_pct_1a5_personas", f"% de unidades de la división {d} ({nombre}) con 1 a 5 personas ocupadas", personas[d]["lowPers"], "%", 1)
            agregar(f"div{d}_pct_mas50_personas", f"% de unidades de la división {d} ({nombre}) con más de 50 personas ocupadas", personas[d]["highPers"], "%", 1)
        agregar(f"div{d}_unidades_pais", f"Unidades de la división {d} ({nombre}) en todo el país", r["unidades_nacional"], "unidades", 0)

    claves_bvn = ["pct_ingreso_bajo", "pct_ingreso_alto", "pct_1a5_personas", "pct_mas50_personas", "ingreso_promedio_millones", "ingreso_total_billones"]
    unidades_bvn = ["%", "%", "%", "%", "millones COP", "billones COP"]
    ws = wb["bogota_vs_nacional"]
    for clave, unidad, (ind, bog, nac) in zip(claves_bvn, unidades_bvn, list(ws.iter_rows(min_row=2, values_only=True))):
        dec = 1 if unidad in ("%", "billones COP") else 0
        agregar(f"bogota_{clave}", f"Bogotá: {ind}", bog, unidad, dec)
        agregar(f"nacional_{clave}", f"País: {ind}", nac, unidad, dec)

    controles = {r[0]: r[1] for r in wb["controles"].iter_rows(min_row=2, values_only=True)}
    agregar("bogota_universo", "Unidades económicas de Bogotá en el módulo de referencia sectorial 2023", controles["Universo Bogotá (visor y API)"], "unidades", 0)
    agregar("bogota_ciiu_visible", "Unidades de Bogotá con división CIIU visible", controles["Bogotá: unidades con división CIIU visible"], "unidades", 0)
    agregar("bogota_ciiu_reserva", "Unidades de Bogotá sin CIIU visible por reserva estadística", controles["Bogotá: CIIU no visible por reserva estadística"], "unidades", 0)
    agregar("nacional_universo", "Unidades económicas del país en el módulo de referencia sectorial 2023", controles["Universo módulo sectoral_reference_2023 · nacional"], "unidades", 0)
    agregar("bogota_pct_unidades_pais", "% de las unidades del país que están en Bogotá", controles["Bogotá: % del total nacional del módulo"], "%", 1)
    agregar("bogota_pct_ingresos_pais", "% de los ingresos 2023 del país que genera Bogotá", controles["Bogotá: % de los ingresos nacionales 2023"], "%", 1)

    for r in wb["bogota_personal_visor"].iter_rows(min_row=2, values_only=True):
        if r[3] == "sin_dato":
            agregar("bogota_pct_sin_info_personal", "% de unidades de Bogotá sin información de personal ocupado", r[1], "%", 1)

    for r in wb["detalle_4dig_visor"].iter_rows(min_row=2, values_only=True):
        codigo, desc, unidades = str(r[0]), r[1], r[2]
        agregar(f"ciiu{codigo}_unidades", f"Unidades en Bogotá de la actividad CIIU {codigo} ({desc})", unidades, "unidades", 0, "Visor Interactivo CENU (Bogotá)")

    for clave, desc, valor, unidad, dec in DERIVADAS:
        agregar(clave, desc, valor, unidad, dec, F_ANALISIS)

    claves = [f["clave"] for f in filas]
    assert len(claves) == len(set(claves)), "claves repetidas"
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    shutil.copyfile(BASE_CONOCIMIENTO, RAIZ / "datos" / "base_conocimiento.txt")
    print(f"{len(filas)} hechos -> {SALIDA.relative_to(RAIZ)}")
    print(f"base de conocimiento -> {(RAIZ / 'datos' / 'base_conocimiento.txt').relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
