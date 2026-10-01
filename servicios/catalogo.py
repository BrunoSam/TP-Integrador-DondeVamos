import bisect
import json
import unicodedata

from estructuras.arbol_binario import ArbolBinarioBusqueda
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
        self._claves = []
        self.indexar()

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
        self.indexar()

    def agregar_lugar(self, lugar):
        """Agrega un lugar a la lista y lo inserta en el árbol.

        No hay que reindexar: el árbol se mantiene al día lugar por lugar, que es
        justamente la ventaja de insertar en O(log n) sin tocar el resto.
        """
        self._lugares.append(lugar)
        self._arbol.insertar(lugar)

    def buscar(self, nombre):
        for lugar in self._lugares:
            if _normalizar(lugar.nombre) == _normalizar(nombre):
                return lugar
        return None

    def ordenar_por_titulo(self):
        """Ordena la lista por nombre normalizado y arma el arreglo de claves."""
        self._lugares.sort(key=lambda l: _normalizar(l.nombre))
        self._claves = [_normalizar(l.nombre) for l in self._lugares]

    def buscar_binaria(self, nombre):
        """Búsqueda binaria sobre la lista ordenada. O(log n)."""
        clave = _normalizar(nombre)
        indice = bisect.bisect_left(self._claves, clave)
        if indice < len(self._claves) and self._claves[indice] == clave:
            return self._lugares[indice]
        return None

    def indexar(self):
        """Construye el BST con los lugares actuales, en orden de carga."""
        self._arbol = ArbolBinarioBusqueda(
            clave=lambda lugar: _normalizar(lugar.nombre)
        )
        for lugar in self._lugares:
            self._arbol.insertar(lugar)

    def buscar_arbol(self, nombre):
        """Búsqueda exacta en el BST. O(log n) promedio. None si no existe."""
        return self._arbol.buscar(_normalizar(nombre))

    def listar_ordenado(self):
        """Lugares en orden alfabético: recorrido inorder del árbol."""
        return self._arbol.inorder()

    def listar_preorder(self):
        """Lugares en preorden (raíz, izq, der): la raíz del árbol primero."""
        return self._arbol.preorder()

    def listar_postorder(self):
        """Lugares en postorden (izq, der, raíz): la raíz del árbol al final."""
        return self._arbol.postorder()

    def altura_arbol(self):
        """Niveles del camino más largo. Sirve para verificar el balance."""
        return self._arbol.altura()

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

    def agregar_salida(self, salida):
        self._salidas.append(salida)

    def listar_salidas(self):
        return list(self._salidas)

    def filtrar(self, categoria):
        return [
            l for l in self._lugares
            if _normalizar(l.categoria) == _normalizar(categoria)
        ]

    def __len__(self):
        return len(self._lugares)