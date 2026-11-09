"""Modelos de lenguaje intercambiables. Todos responden JSON con generar_json().

- GeminiModelo y OpenAIModelo: los reales, para las mediciones del sábado.
- ModeloComprometido: un simulador del PEOR CASO. Siempre obedece las instrucciones escondidas en
  los documentos. No mide a la IA: sirve para probar que la compuerta aguanta aunque el modelo
  esté totalmente manipulado (la tesis de AgentBreak) y para probar todo sin internet ni créditos.
  Sus resultados nunca se reportan como resultados de un modelo real.
"""

import base64
import hashlib
import json
import os
import re
import unicodedata
from pathlib import Path

CACHE = Path(__file__).resolve().parents[1] / "resultados" / "cache_llm"


def _sin_tildes(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn")


class _ConCache:
    """Guarda cada respuesta en disco: la misma consulta no se paga dos veces."""

    nombre = "modelo"

    def generar_json(self, sistema: str, usuario: str, imagen: bytes | None = None, texto_imagen: str | None = None) -> dict:
        llave = hashlib.sha256(json.dumps([self.nombre, sistema, usuario,
                                           hashlib.sha256(imagen or b"").hexdigest()]).encode()).hexdigest()[:24]
        ruta = CACHE / f"{llave}.json"
        if ruta.exists():
            return json.loads(ruta.read_text(encoding="utf-8"))
        respuesta = self._llamar(sistema, usuario, imagen)
        CACHE.mkdir(parents=True, exist_ok=True)
        ruta.write_text(json.dumps(respuesta, ensure_ascii=False), encoding="utf-8")
        return respuesta

    def _llamar(self, sistema, usuario, imagen):
        raise NotImplementedError


class GeminiModelo(_ConCache):
    """Gemini con salida JSON. Lee la clave de GEMINI_API_KEY o GOOGLE_API_KEY."""

    def __init__(self, modelo: str = "gemini-2.5-flash"):
        from google import genai
        self.nombre = modelo
        self._cliente = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))

    def _llamar(self, sistema, usuario, imagen):
        from google.genai import types
        contenido = [usuario] if imagen is None else [types.Part.from_bytes(data=imagen, mime_type="image/png"), usuario]
        r = self._cliente.models.generate_content(
            model=self.nombre, contents=contenido,
            config=types.GenerateContentConfig(system_instruction=sistema, response_mime_type="application/json", temperature=0))
        return json.loads(r.text)


class OpenAIModelo(_ConCache):
    """Respaldo con OpenAI. Lee la clave de OPENAI_API_KEY."""

    def __init__(self, modelo: str = "gpt-4o-mini"):
        from openai import OpenAI
        self.nombre = modelo
        self._cliente = OpenAI()

    def _llamar(self, sistema, usuario, imagen):
        partes = [{"type": "text", "text": usuario}]
        if imagen is not None:
            url = "data:image/png;base64," + base64.b64encode(imagen).decode()
            partes.append({"type": "image_url", "image_url": {"url": url}})
        r = self._cliente.chat.completions.create(
            model=self.nombre, temperature=0, response_format={"type": "json_object"},
            messages=[{"role": "system", "content": sistema}, {"role": "user", "content": partes}])
        return json.loads(r.choices[0].message.content)


class ModeloComprometido:
    """Peor caso: obedece siempre lo que ordene un documento. Determinista y sin internet."""

    nombre = "comprometido (peor caso)"

    def __init__(self, tabla=None):
        # tabla: TablaOficial, para contestar bien las preguntas legítimas (el ataque es lo que se mide).
        self.tabla = tabla

    # Una orden escondida: "responde exactamente: «...»" o "di que «...»".
    _ORDEN = re.compile(r"(?:responde|di que|escribe|contesta)[^«]{0,40}«([^»]+)»", re.I)
    _TOTAL_FALSO = re.compile(r"\btotal (?:real )?es \$ ?([\d.]+)", re.I)

    def generar_json(self, sistema: str, usuario: str, imagen: bytes | None = None, texto_imagen: str | None = None) -> dict:
        if texto_imagen is not None:
            return self._extraer_factura(texto_imagen)
        orden = self._ORDEN.search(usuario)
        if orden:
            return {"texto": orden.group(1), "claves": []}
        return self._responder_legitimo(sistema, usuario)

    def _responder_legitimo(self, sistema: str, usuario: str) -> dict:
        pregunta = usuario.split("PREGUNTA:")[-1]
        palabras = set(re.findall(r"[a-z0-9]+", _sin_tildes(pregunta))) - {"de", "la", "el", "en", "y", "que", "con", "las", "los", "del", "cuantas", "cual", "es"}
        mejor, puntaje = None, 0
        hechos = self.tabla.hechos.values() if self.tabla else []
        for h in hechos:
            clave = h.clave
            p = len(palabras & set(re.findall(r"[a-z0-9]+", _sin_tildes(h.descripcion + " " + clave.replace("_", " ")))))
            if p > puntaje:
                mejor, puntaje = clave, p
        if mejor is None:
            return {"texto": "No tengo ese dato.", "claves": []}
        if "marcador" in sistema.lower():
            return {"texto": f"Según el CENU (resultados preliminares, año de referencia 2023): {{{mejor}}}.", "claves": [mejor]}
        return {"texto": f"Según el CENU (resultados preliminares, año de referencia 2023): {self.tabla.hechos[mejor].texto()}.", "claves": [mejor]}

    def _extraer_factura(self, texto: str) -> dict:
        def campo(etiqueta):
            m = re.search(rf"{etiqueta}\s*:?\s*\$?\s*([\d.]+)", texto, re.I)
            return int(m.group(1).replace(".", "")) if m else None
        nit = re.search(r"NIT\s*:?\s*([\d.]+-\d)", texto)
        datos = {"nit": nit.group(1) if nit else None, "subtotal": campo("SUBTOTAL"),
                 "iva": campo(r"IVA \(19 ?%\)"), "total": campo(r"TOTAL A PAGAR")}
        falso = self._TOTAL_FALSO.search(texto)
        if falso:  # obedece la instrucción escondida
            datos["total"] = int(falso.group(1).replace(".", ""))
            sub = re.search(r"subtotal (?:real )?es \$ ?([\d.]+)", texto, re.I)
            iva = re.search(r"iva (?:real )?es \$ ?([\d.]+)", texto, re.I)
            if sub:
                datos["subtotal"] = int(sub.group(1).replace(".", ""))
            if iva:
                datos["iva"] = int(iva.group(1).replace(".", ""))
        return datos


def crear_modelo(nombre: str, tabla=None):
    """'comprometido', 'gemini', 'gemini:gemini-2.5-pro', 'openai' u 'openai:gpt-4o'."""
    proveedor, _, version = nombre.partition(":")
    if proveedor == "comprometido":
        return ModeloComprometido(tabla)
    if proveedor == "gemini":
        return GeminiModelo(version or "gemini-2.5-flash")
    if proveedor == "openai":
        return OpenAIModelo(version or "gpt-4o-mini")
    raise ValueError(f"Modelo desconocido: {nombre}")
