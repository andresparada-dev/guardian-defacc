"""Defensa 3: verificadores en código normal y la compuerta que decide qué sale.

Los verificadores no usan IA. La compuerta tiene tres modos:
- "apagada": todo sale tal como lo propuso el agente (línea base).
- "aviso":   sale igual, pero con una advertencia visible. Así funciona hoy el verificador
             jurídico de SAPHEN.
- "bloqueo": si un verificador falla, la respuesta se reemplaza (cifras) o la factura se
             manda a revisión humana (facturas). Así funciona el verificador de Vigía en SAPHEN.
"""

from dataclasses import dataclass, field

from .hechos import TablaOficial
from .numeros import extraer_numeros

MODOS = ("apagada", "aviso", "bloqueo")
RESPUESTA_BLOQUEADA = ("No tengo ese dato verificado en las cifras oficiales del CENU. "
                       "Puedes consultarlo en el Visor Interactivo del DANE.")


@dataclass
class Verificacion:
    ok: bool
    problemas: list[str] = field(default_factory=list)


def verificar_cifras(texto: str, tabla: TablaOficial, pregunta: str = "") -> Verificacion:
    """Toda cifra de la respuesta debe estar en la tabla oficial, ser estructural o venir de la pregunta."""
    de_la_pregunta = {round(n, 2) for n in extraer_numeros(pregunta)}
    problemas = [f"La cifra {n:g} no está en la tabla oficial"
                 for n in extraer_numeros(texto)
                 if not tabla.es_permitido(n) and round(n, 2) not in de_la_pregunta]
    return Verificacion(ok=not problemas, problemas=problemas)


def compuerta_respuesta(modo: str, texto: str, verificacion: Verificacion) -> tuple[str, str]:
    """Devuelve (texto que ve la persona, estado). Estado: 'entregada', 'entregada_con_aviso' o 'bloqueada'."""
    if modo not in MODOS:
        raise ValueError(f"Modo desconocido: {modo}")
    if modo == "apagada" or verificacion.ok:
        return texto, "entregada"
    if modo == "aviso":
        return texto + "\n\n⚠️ Aviso: esta respuesta tiene cifras que no coinciden con la fuente oficial.", "entregada_con_aviso"
    return RESPUESTA_BLOQUEADA, "bloqueada"
