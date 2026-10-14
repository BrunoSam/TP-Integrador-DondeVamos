import bisect
import json
import time
import unicodedata

from estructuras.arbol_avl import ArbolAVL
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
        """Agrega un lugar a la lista y lo inserta en ambos árboles.

        No hay que reindexar: los árboles se mantienen al día lugar por lugar,
        que es justamente la ventaja de insertar en O(log n) sin tocar el resto.
        """
        self._lugares.append(lugar)
        self._arbol.insertar(lugar)
        self._avl.insertar(lugar)

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
        """Construye el BST y el AVL con los lugares actuales, en orden de carga.

        El AVL se arma sobre el mismo orden, pero eso ya no importa: se
        rebalancea solo, así que la altura queda en O(log n) sin importar cómo
        lleguen las claves. El BST se conserva como término de comparación.
        """
        self._arbol = ArbolBinarioBusqueda(
            clave=lambda lugar: _normalizar(lugar.nombre)
        )
        self._avl = ArbolAVL(clave=lambda lugar: _normalizar(lugar.nombre))
        for lugar in self._lugares:
            self._arbol.insertar(lugar)
            self._avl.insertar(lugar)

    def buscar_arbol(self, nombre):
        """Búsqueda exacta en el BST. O(log n) promedio. None si no existe."""
        return self._arbol.buscar(_normalizar(nombre))

    def buscar_avl(self, nombre):
        """Búsqueda exacta en el AVL. O(log n) garantizado. None si no existe."""
        return self._avl.buscar(_normalizar(nombre))

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
        """Niveles del camino más largo del BST. Sirve para verificar el balance."""
        return self._arbol.altura()

    def altura_avl(self):
        """Altura del AVL. Siempre O(log n), sin importar el orden de carga."""
        return self._avl.altura()

    def comparar_bst_vs_avl(self):
        """Demo del TP4: mide BST y AVL con los mismos lugares insertados en
        orden alfabético, que es el peor caso del BST sin balancear.

        Devuelve, por etiqueta, la altura resultante y el tiempo de construcción
        en milisegundos. La construcción se paga una sola vez y es lo que deja
        en evidencia la degeneración del BST frente al AVL.
        """
        ordenados = sorted(self._lugares, key=lambda l: _normalizar(l.nombre))
        resultado = {}
        for etiqueta, arbol in (
            ("BST", ArbolBinarioBusqueda(clave=lambda l: _normalizar(l.nombre))),
            ("AVL", ArbolAVL(clave=lambda l: _normalizar(l.nombre))),
        ):
            inicio = time.perf_counter()
            for lugar in ordenados:
                arbol.insertar(lugar)
            resultado[etiqueta] = {
                "altura": arbol.altura(),
                "ms": (time.perf_counter() - inicio) * 1000,
            }
        return resultado

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