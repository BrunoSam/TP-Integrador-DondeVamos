import json
import unicodedata

from modelos.lugar import Lugar
from modelos.salida import Salida


def _normalizar(texto):
    """Minúsculas y sin tildes: 'Gastronomía' ~ 'gastronomia'."""
    texto = texto.lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


class Catalogo:
    """Lógica de negocio: carga y operaciones sobre el catálogo de lugares."""

    def __init__(self):
        self._lugares = []
        self._salidas = []

    def cargar_desde_json(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for item in datos:
            self._lugares.append(
                Lugar(
                    item["id"],
                    item["nombre"],
                    item["zona"],
                    item["categoria"],
                    item["puntuacion"],
                    item["horario_apertura"],
                    item["horario_cierre"],
                    item["costo"],
                )
            )

    def buscar(self, nombre):
        for lugar in self._lugares:
            if _normalizar(lugar.nombre) == _normalizar(nombre):
                return lugar
        return None

    def buscar_parcial(self, texto):
        """Búsqueda por coincidencia parcial: 'café' encuentra 'Café Tortoni'."""
        texto = _normalizar(texto)
        return [
            lugar for lugar in self._lugares
            if texto in _normalizar(lugar.nombre)
        ]

    def listar(self):
        return list(self._lugares)

    def cargar_salidas_desde_json(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for item in datos:
            self._salidas.append(
                Salida(
                    item["id"],
                    item["nombre"],
                    item["participantes"],
                )
            )

    def listar_salidas(self):
        return list(self._salidas)

    def filtrar(self, categoria):
        return [
            l for l in self._lugares
            if _normalizar(l.categoria) == _normalizar(categoria)
        ]

    def __len__(self):
        return len(self._lugares)