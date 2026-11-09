"""Pruebas del manejo de cuota para planes gratuitos. Sin internet: usan un modelo falso."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from guardian import llm  # noqa: E402
from guardian import escenario_cifras as A  # noqa: E402
from guardian.hechos import TablaOficial  # noqa: E402
from guardian.medidor import PRESETS, estimar_llamadas, medir_cifras, seleccionar_casos, seleccionar_facturas  # noqa: E402


class ModeloFalso(llm._ConCache):
    """Responde siempre lo mismo; puede fallar con un 429 las primeras veces."""

    nombre = "falso"

    def __init__(self, errores=()):
        self.errores = list(errores)
        self.reales = 0

    def _llamar(self, sistema, usuario, imagen):
        self.reales += 1
        if self.errores:
            raise RuntimeError(self.errores.pop(0))
        return {"texto": "No tengo ese dato.", "claves": []}


@pytest.fixture(autouse=True)
def sin_esperas_y_cache_temporal(monkeypatch, tmp_path):
    monkeypatch.setattr(llm, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)


def test_tope_de_llamadas_y_la_cache_no_cuenta():
    m = ModeloFalso()
    m.max_llamadas = 2
    m.generar_json("s", "u1")
    m.generar_json("s", "u1")  # caché: no cuenta
    m.generar_json("s", "u2")
    with pytest.raises(llm.SinCuota):
        m.generar_json("s", "u3")
    assert m.reales == 2


def test_reintenta_el_limite_por_minuto():
    m = ModeloFalso(errores=["429 RESOURCE_EXHAUSTED. Please retry in 3s"])
    assert m.generar_json("s", "u") == {"texto": "No tengo ese dato.", "claves": []}
    assert m.reales == 2


def test_cuota_diaria_detiene_sin_reintentar():
    m = ModeloFalso(errores=["429 RESOURCE_EXHAUSTED: GenerateRequestsPerDayPerProjectPerModel-FreeTier"])
    with pytest.raises(llm.SinCuota):
        m.generar_json("s", "u")
    assert m.reales == 1


def test_medicion_se_detiene_limpia_y_resume_casos_completos():
    tabla = TablaOficial()
    m = ModeloFalso()
    m.max_llamadas = 3
    casos = seleccionar_casos(A.cargar_casos(), n_ataques=3, n_legitimas=2)
    detalle, resumen, hechos, total = medir_cifras(m, tabla, casos, PRESETS["minimo"])
    assert (hechos, total) == (3, 5)  # preset mínimo: 1 llamada por caso
    assert all(r["ataques_total"] + r["legitimas_total"] == 3 for r in resumen)


def test_estimacion_y_muestras():
    assert estimar_llamadas(PRESETS["minimo"], 8, 12) == 20
    assert estimar_llamadas(PRESETS["completo"], 8, 12) == 3 * 8 + 2 * 12
    lote = [{"variante": v, "numero": f"{v}-{i}"} for v in ("limpia", "trampa_visible", "trampa_margen") for i in range(3)]
    elegidas = seleccionar_facturas(lote, 4)
    assert [e["variante"] for e in elegidas] == ["trampa_visible", "trampa_margen", "limpia", "trampa_visible"]
