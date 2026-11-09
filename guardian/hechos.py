"""Tabla de cifras oficiales: la fuente de verdad del guardián.

Cada hecho tiene una clave (div47_unidades), una descripción, un valor, una unidad y su fuente.
El agente puede citar un hecho por su clave entre llaves ({div47_unidades}) y el código pone
el número: así la cifra nunca la escribe el modelo (defensa 2).
"""

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from .numeros import formatear

RUTA_HECHOS = Path(__file__).resolve().parents[1] / "datos" / "hechos_oficiales.csv"

# Números que aparecen en respuestas correctas pero no son estadísticas: años, límites de los
# rangos del CENU y conteos pequeños ("las 10 divisiones", "3 divisiones"). Es un límite
# conocido: una cifra falsa que coincida con uno de estos números no se detecta.
NUMEROS_ESTRUCTURALES = {2023.0, 2024.0, 2025.0, 2026.0, 1993.0,
                         0.0, 5.0, 6.0, 10.0, 11.0, 20.0, 21.0, 50.0, 51.0, 100.0, 101.0, 500.0, 501.0,
                         1000.0, 1001.0, 5000.0, 10000.0, 100000.0}
NUMEROS_ESTRUCTURALES |= {float(n) for n in range(1, 13)}

_MARCADOR = re.compile(r"\{([a-z0-9_]+)\}")


@dataclass(frozen=True)
class Hecho:
    clave: str
    descripcion: str
    valor: float
    unidad: str
    decimales: int
    fuente: str

    def texto(self) -> str:
        """El valor listo para mostrar: '92.335 unidades', '47,2 %', '1.180,4 billones de pesos'."""
        numero = formatear(self.valor, self.decimales)
        if self.unidad == "%":
            return f"{numero} %"
        if self.unidad.endswith("COP"):
            return f"{numero} {self.unidad.replace(' COP', '')} de pesos"
        return f"{numero} {self.unidad}"


class TablaOficial:
    def __init__(self, ruta: Path = RUTA_HECHOS):
        with Path(ruta).open(encoding="utf-8") as fh:
            self.hechos = {f["clave"]: Hecho(f["clave"], f["descripcion"], float(f["valor"]), f["unidad"],
                                             int(f["decimales"]), f["fuente"]) for f in csv.DictReader(fh)}
        # Códigos CIIU que aparecen en la tabla (47, 4781...): son identificadores, no cifras.
        codigos = set()
        for clave in self.hechos:
            m = re.match(r"(?:div|ciiu)(\d+)_", clave)
            if m:
                codigos.add(float(m.group(1)))
        self._permitidos = set(NUMEROS_ESTRUCTURALES) | codigos
        for h in self.hechos.values():
            # Se aceptan el valor exacto y sus redondeos habituales (47,17 se puede decir 47,2 o 47).
            for v in (h.valor, round(h.valor, 1), round(h.valor)):
                self._permitidos.add(round(float(v), 2))

    def es_permitido(self, numero: float) -> bool:
        return round(numero, 2) in self._permitidos or round(numero, 1) in self._permitidos

    def catalogo(self) -> str:
        """Lista de claves con su descripción, SIN valores, para que el modelo elija qué citar."""
        return "\n".join(f"- {h.clave}: {h.descripcion}" for h in self.hechos.values())

    def poner_cifras(self, texto: str) -> tuple[str, list[str]]:
        """Reemplaza {clave} por el valor oficial. Devuelve el texto y las claves que no existen."""
        desconocidas = []

        def reemplazo(m):
            h = self.hechos.get(m.group(1))
            if h is None:
                desconocidas.append(m.group(1))
                return "[dato no disponible]"
            return h.texto()

        return _MARCADOR.sub(reemplazo, texto), desconocidas
