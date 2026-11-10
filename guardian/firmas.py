"""Capa de firmas: un detector de intrusos (IDS) para los documentos que lee el agente.

Funciona como un antivirus o un IDS basado en firmas: antes de que la IA lea un documento, el
código busca en su texto patrones conocidos de ataque. Si encuentra una firma, el documento queda
en cuarentena y la IA no lo ve. Cada firma tiene un código y una descripción, así que siempre se
sabe qué regla saltó y por qué.

De dónde salen las firmas: de plantillas públicas de inyección de instrucciones (los ataques de
AgentDojo como "ignore previous instructions" o "important instructions", y los ejemplos de
OWASP LLM01) y de las frases típicas de fraude con facturas. No se escribieron a partir de los
ataques reescritos sin orden (A11 a A15) ni del grupo de ataques que se escribe el sábado.

Ventajas: es rápida, no gasta llamadas a la IA y explica lo que bloquea.
Límite, el mismo de cualquier IDS por firmas: solo atrapa ataques parecidos a los conocidos. Un
dato falso escrito como afirmación, sin ninguna orden, pasa. Por eso va junto a las reglas del
código (defensa 3), que no dependen de cómo esté escrito el ataque.
"""

import re
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class Firma:
    id: str
    descripcion: str
    patron: re.Pattern


def _firma(id_: str, descripcion: str, patron: str) -> Firma:
    return Firma(id_, descripcion, re.compile(patron, re.I))


# Los patrones se buscan sobre el texto en minúsculas, sin tildes y con los saltos de línea
# convertidos en espacios (la lectura por OCR parte las frases en renglones).
FIRMAS: tuple[Firma, ...] = (
    _firma("F01", "Pide ignorar u olvidar las instrucciones o reglas",
           r"\b(ignor|olvid|omit|descart|desobedec|disregard|forget)\w*\b[^.]{0,40}\b(instruccion|indicacion|regla|instruction|rule|prompt)"),
    _firma("F02", "Anuncia instrucciones nuevas o un cambio de rol",
           r"\b(nuevas? instrucciones?|new instructions?|a partir de ahora|from now on|en adelante debes|ahora eres|you are now|actua como|act as)\b"),
    _firma("F03", "Ordena responder con un texto exacto",
           r"\b(responde|responda|contesta|conteste|escribe|escriba|repite|repita|di|diga|answer|reply|respond|say|write|repeat)\b"
           r"[^.]{0,25}\b(exactamente|textualmente|literalmente|unicamente|solamente|exactly|verbatim|literally)\b"),
    _firma("F04", "Ordena decir una frase entre comillas",
           r"\b(responde|responda|contesta|conteste|escribe|escriba|di|diga|dile|answer|say)\b(\s+que)?\s*:?\s*[«\"“]"),
    _firma("F05", "Mensaje dirigido al asistente, al sistema o a la IA",
           r"\b(instruccion|nota|mensaje|orden|aviso|indicacion|message|note|instruction)\w*\b(\s+\w+){0,3}\s+"
           r"(para|al|a la|to|for)\s+(el\s+|la\s+|the\s+)?(asistente|sistema|modelo|ia|agente|chatbot|bot|assistant|system|model|ai|agent|llm)\b"),
    _firma("F06", "Pide revelar la configuración, el prompt o una clave",
           r"\b(codigo interno|configuracion interna|codigo de configuracion|instrucciones (del|de) sistema|prompt (del|de) sistema"
           r"|system prompt|tus instrucciones|your (system )?instructions|contrasena|password|clave de api|api key)\b"),
    _firma("F07", "Marcadores de plantillas de ataque conocidas",
           r"(<\s*/?\s*information\s*>|#{2,}\s*\(?\s*system|\[\s*/?\s*(system|sistema|inst)\s*\]|<\|im_(start|end)\|>"
           r"|mensaje importante de mi parte|this is an important message from me)"),
    _firma("F08", "Pide hacer algo antes de responder (plantilla 'important instructions')",
           r"\b(antes de (responder|contestar|resolver|continuar|seguir)|before you (can )?(answer|solve|respond|continue))\b"),
    _firma("F09", "Frases de fraude con facturas",
           r"(sistema de ia|nota para el sistema|para la ia|instruccion para|aprobar sin revisi|ignora"
           r"|\b(aprobar|aprueba|apruebe|approve)\w*\s+sin\s+(revision|verificacion|control|validacion)"
           r"|\b(total|subtotal|iva|valor)\s+(real|correcto|verdadero|actualizado)\s+es\b)"),
)


def normalizar(texto: str) -> str:
    sin_tildes = "".join(c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", sin_tildes)


def buscar_firmas(texto: str) -> list[str]:
    """Los códigos de las firmas que aparecen en el texto (lista vacía si está limpio)."""
    t = normalizar(texto or "")
    return [f.id for f in FIRMAS if f.patron.search(t)]


def describir(ids: list[str]) -> str:
    nombres = {f.id: f.descripcion for f in FIRMAS}
    return "; ".join(f"{i} ({nombres[i]})" for i in ids)


def revisar_documentos(documentos: list[dict]) -> tuple[list[dict], list[dict]]:
    """Separa los documentos limpios de los que van a cuarentena. Devuelve (limpios, cuarentena)."""
    limpios, cuarentena = [], []
    for d in documentos:
        ids = buscar_firmas(d["texto"])
        if ids:
            cuarentena.append({"id": d["id"], "firmas": ids})
        else:
            limpios.append(d)
    return limpios, cuarentena
