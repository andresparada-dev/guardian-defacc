"""El medidor: corre todos los casos en cada combinación de defensas y resume los resultados.

Métricas por configuración:
- Escenario A (cifras): % de ataques que llegan a la persona, % de preguntas legítimas bien
  respondidas y preguntas legítimas bloqueadas por error (falsos positivos).
- Escenario B (facturas): % de facturas con trampa aprobadas solas, facturas alteradas aprobadas,
  % de facturas limpias bien decididas y limpias mandadas a revisión por error.

Con el modelo comprometido los resultados miden la COMPUERTA en el peor caso, no a la IA.
"""

import csv
from datetime import datetime
from pathlib import Path

from . import escenario_cifras as A
from . import escenario_facturas as B
from .facturas import cargar_lote
from .hechos import TablaOficial
from .ocr import leer_texto

CONFIGURACIONES = [  # (etiqueta, defensas, modo de la compuerta)
    ("Sin defensa", set(), "apagada"),
    ("D1 delimitar", {"d1"}, "apagada"),
    ("D1+D2 forma fija", {"d1", "d2"}, "apagada"),
    ("D1+D2+D3 aviso", {"d1", "d2"}, "aviso"),
    ("D1+D2+D3 bloqueo", {"d1", "d2"}, "bloqueo"),
]


def _pct(a: int, b: int) -> float:
    return round(100 * a / b, 1) if b else 0.0


def medir_cifras(modelo, tabla: TablaOficial, casos: dict, configuraciones=CONFIGURACIONES) -> tuple[list[dict], list[dict]]:
    fragmentos = A.cargar_fragmentos()
    detalle, resumen = [], []
    for etiqueta, defensas, modo in configuraciones:
        exitos = correctas = bloqueadas = 0
        for c in casos["legitimas"]:
            r = A.responder(c["pregunta"], modelo, tabla, defensas, modo, fragmentos=fragmentos)
            ok = A.respuesta_correcta(c, r, tabla)
            correctas += ok
            bloqueadas += r["estado"] != "entregada"
            detalle.append({"config": etiqueta, "caso": c["id"], "tipo": "legitima", "familia": "", "ok": ok, **r})
        for a in casos["ataques"]:
            trampa = {"id": f"trampa-{a['id']}", "texto": a["documento"]}
            r = A.responder(a["pregunta"], modelo, tabla, defensas, modo, documentos_extra=[trampa], fragmentos=fragmentos)
            exito = A.ataque_exitoso(a, r)
            exitos += exito
            detalle.append({"config": etiqueta, "caso": a["id"], "tipo": "ataque", "familia": a["familia"], "ok": not exito, **r})
        n_l, n_a = len(casos["legitimas"]), len(casos["ataques"])
        resumen.append({"escenario": "A · cifras", "config": etiqueta, "ataques_exitosos": exitos, "ataques_total": n_a,
                        "pct_ataques_exitosos": _pct(exitos, n_a), "legitimas_bien": correctas, "legitimas_total": n_l,
                        "pct_legitimas_bien": _pct(correctas, n_l), "falsos_positivos": bloqueadas})
    return detalle, resumen


def medir_facturas(modelo, carpeta: Path, configuraciones=CONFIGURACIONES, ocr: str = "real") -> tuple[list[dict], list[dict]]:
    """ocr: 'real' (Tesseract si está instalado), 'simulado' (texto impreso, solo para pruebas) o 'no'."""
    lote = cargar_lote(carpeta)
    textos_ocr = {}
    for meta in lote:
        if ocr == "real":
            textos_ocr[meta["numero"]] = leer_texto(carpeta / f"{meta['numero']}.png")
        elif ocr == "simulado":
            textos_ocr[meta["numero"]] = "\n".join(meta["texto_impreso"])
        else:
            textos_ocr[meta["numero"]] = None
    detalle, resumen = [], []
    for etiqueta, defensas, modo in configuraciones:
        trampas = [m for m in lote if m["variante"].startswith("trampa")]
        alteradas = [m for m in lote if m["variante"] == "alterada"]
        limpias = [m for m in lote if m["variante"] == "limpia"]
        aprobadas_trampa = aprobadas_alteradas = limpias_bien = limpias_fp = 0
        for meta in lote:
            # La segunda lectura por OCR es parte de la defensa 3: solo se usa cuando la compuerta está prendida.
            texto_ocr = textos_ocr[meta["numero"]] if modo != "apagada" else None
            r = B.procesar(carpeta / f"{meta['numero']}.png", meta, modelo, defensas, modo, texto_ocr)
            if meta in trampas:
                aprobadas_trampa += r["decision"] == "aprobar"
            elif meta in alteradas:
                aprobadas_alteradas += r["decision"] == "aprobar"
            else:
                limpias_bien += r["decision"] == r["esperado"]
                limpias_fp += r["esperado"] == "aprobar" and r["decision"] != "aprobar"
            detalle.append({"config": etiqueta, **{k: v for k, v in r.items() if k != "datos"}, "datos": r["datos"]})
        resumen.append({"escenario": "B · facturas", "config": etiqueta, "ataques_exitosos": aprobadas_trampa,
                        "ataques_total": len(trampas), "pct_ataques_exitosos": _pct(aprobadas_trampa, len(trampas)),
                        "alteradas_aprobadas": aprobadas_alteradas, "legitimas_bien": limpias_bien,
                        "legitimas_total": len(limpias), "pct_legitimas_bien": _pct(limpias_bien, len(limpias)),
                        "falsos_positivos": limpias_fp})
    return detalle, resumen


def _guardar_csv(filas: list[dict], ruta: Path) -> None:
    if not filas:
        return
    campos = list(dict.fromkeys(k for f in filas for k in f))
    with ruta.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)


def graficar(resumen: list[dict], ruta: Path, nombre_modelo: str) -> None:
    """Dos paneles (A y B), misma escala: % de ataques que llegan a la persona en cada configuración."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    escenarios = list(dict.fromkeys(r["escenario"] for r in resumen))
    fig, ejes = plt.subplots(1, len(escenarios), figsize=(6.2 * len(escenarios), 4.4), sharey=True, squeeze=False)
    for ax, esc in zip(ejes[0], escenarios):
        filas = [r for r in resumen if r["escenario"] == esc]
        x = range(len(filas))
        valores = [r["pct_ataques_exitosos"] for r in filas]
        ax.bar(x, valores, color="#2a78d6", width=0.62, zorder=2)
        for i, v in enumerate(valores):
            ax.text(i, v + 2, f"{v:g} %", ha="center", va="bottom", fontsize=10, color="#0b0b0b")
        ax.set_xticks(list(x), [r["config"].replace(" ", "\n", 1) + f"\nFP: {r['falsos_positivos']}" for r in filas], fontsize=8.5)
        ax.set_ylim(0, 110)
        ax.set_title(esc, fontsize=11, loc="left", color="#0b0b0b")
        ax.grid(axis="y", color="#e1e0d9", linewidth=0.8, zorder=0)
        for lado in ("top", "right", "left"):
            ax.spines[lado].set_visible(False)
        ax.spines["bottom"].set_color("#c3c2b7")
        ax.tick_params(axis="y", colors="#6b6a64", length=0)
    ejes[0][0].set_ylabel("% de ataques que llegan a la persona", color="#3d3d3a")
    if nombre_modelo.startswith("comprometido"):
        titulo = "Ataques que llegan a la persona · peor caso simulado: mide la compuerta, no a la IA"
    else:
        titulo = f"Ataques que llegan a la persona · modelo {nombre_modelo}"
    fig.suptitle(titulo, fontsize=10.5, x=0.01, ha="left")
    fig.text(0.01, 0.005, "FP = respuestas o facturas legítimas bloqueadas por error. Menos es mejor en las dos medidas.", fontsize=8, color="#6b6a64")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(ruta, dpi=160)
    plt.close(fig)


def correr_todo(modelo, nombre_modelo: str, carpeta_facturas: Path | None, salida_base: Path, ocr: str = "real",
                escenarios: tuple[str, ...] = ("A", "B")) -> Path:
    tabla = TablaOficial()
    marca = datetime.now().strftime("%Y%m%d-%H%M%S")
    salida = salida_base / f"{marca}_{nombre_modelo.split()[0].replace(':', '-')}"
    salida.mkdir(parents=True, exist_ok=True)
    resumen = []
    if "A" in escenarios:
        det, res = medir_cifras(modelo, tabla, A.cargar_casos())
        _guardar_csv(det, salida / "detalle_cifras.csv")
        resumen += res
    if "B" in escenarios and carpeta_facturas is not None:
        det, res = medir_facturas(modelo, carpeta_facturas, ocr=ocr)
        _guardar_csv(det, salida / "detalle_facturas.csv")
        resumen += res
    _guardar_csv(resumen, salida / "resumen.csv")
    graficar(resumen, salida / "grafico_ataques.png", nombre_modelo)
    lineas = [f"# Resultados · modelo {nombre_modelo} · OCR {ocr}", ""]
    if nombre_modelo.startswith("comprometido"):
        lineas += ["> Peor caso simulado: el modelo obedece todas las trampas. Mide la compuerta, no a la IA.", ""]
    lineas += ["| Escenario | Configuración | Ataques exitosos | Legítimas bien | Falsos positivos |", "|---|---|---|---|---|"]
    for r in resumen:
        lineas.append(f"| {r['escenario']} | {r['config']} | {r['ataques_exitosos']}/{r['ataques_total']} ({r['pct_ataques_exitosos']:g} %) | "
                      f"{r['legitimas_bien']}/{r['legitimas_total']} | {r['falsos_positivos']} |")
    (salida / "resumen.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return salida
