
class _ItemPrioridad:
    def __init__(self, prioridad, desempate, elemento):
        self.prioridad = prioridad
        self.desempate = desempate
        self.elemento = elemento

    def __lt__(self, otro):
        if self.prioridad != otro.prioridad:
            return self.prioridad < otro.prioridad
        return self.desempate < otro.desempate

    def __gt__(self, otro):
        if self.prioridad != otro.prioridad:
            return self.prioridad > otro.prioridad
        return self.desempate > otro.desempate

    def __eq__(self, otro):
        return self.prioridad == otro.prioridad and self.desempate == otro.desempate
from estructuras.heap_binario import HeapBinario
import bisect
import json
import time
import unicodedata

from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_binario import ArbolBinarioBusqueda
from estructuras.arbol_general import ArbolGeneral
from modelos.lugar import Lugar
from modelos.salida import Salida


def _normalizar(texto):
    """Minúsculas y sin tildes: 'Gastronomía' ~ 'gastronomia'."""
    texto = texto.lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


RAIZ_POR_DEFECTO = "Dónde vamos"
GRUPO_OTROS = "Otros"
SEPARADOR_RUTA = " > "


class Catalogo:
    """Lógica de negocio: carga y operaciones sobre el catálogo de lugares."""

    def __init__(self):
        self._lugares = []
        self._salidas = []
        self._claves = []
        # Jerarquía de categorías (TP5): se define antes de indexar() porque
        # indexar() también arma ese árbol.
        self._nombre_raiz = RAIZ_POR_DEFECTO
        self._taxonomia = {}
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
        """Agrega un lugar a la lista, a ambos árboles y a la jerarquía de categorías.

        No hay que reindexar: los árboles se mantienen al día lugar por lugar,
        que es justamente la ventaja de insertar en O(log n) sin tocar el resto.
        """
        self._lugares.append(lugar)
        self._arbol.insertar(lugar)
        self._avl.insertar(lugar)
        self._colgar_lugar(lugar)

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
        self._construir_arbol_categorias()

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

    # --- Jerarquía de categorías (TP5) --------------------------------------

    def cargar_categorias_desde_json(self, ruta):
        """Carga la jerarquía de grupos y categorías y rearma el árbol.

        El archivo tiene la forma {"raiz": ..., "grupos": {grupo: [categorías]}}.
        Los nombres se comparan sin tildes ni mayúsculas, así que "Cafetería"
        engancha con los lugares de categoría "cafeteria".
        """
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        self._nombre_raiz = datos.get("raiz", RAIZ_POR_DEFECTO)
        self._taxonomia = {
            grupo: list(categorias)
            for grupo, categorias in datos.get("grupos", {}).items()
        }
        self._construir_arbol_categorias()

    def _construir_arbol_categorias(self):
        """Arma raíz > grupos > categorías y cuelga cada lugar de su categoría.

        Sin jerarquía cargada, las categorías cuelgan directo de la raíz: el
        árbol existe igual y se arma solo con los datos. Una categoría que no
        figura en la jerarquía cargada va al grupo "Otros", así que ningún
        lugar queda afuera del árbol.
        """
        arbol = ArbolGeneral(self._nombre_raiz, clave=_normalizar)
        self._arbol_categorias = arbol
        self._nodos_grupo = {}
        self._nodos_categoria = {}
        for grupo, categorias in self._taxonomia.items():
            nodo_grupo = arbol.agregar(arbol.raiz, grupo)
            self._nodos_grupo[_normalizar(grupo)] = nodo_grupo
            for categoria in categorias:
                self._nodos_categoria[_normalizar(categoria)] = arbol.agregar(
                    nodo_grupo, categoria
                )
        for lugar in self._lugares:
            self._colgar_lugar(lugar)

    def _colgar_lugar(self, lugar):
        """Cuelga el lugar como hoja de su categoría, creándola si hace falta."""
        arbol = self._arbol_categorias
        clave = _normalizar(lugar.categoria)
        nodo = self._nodos_categoria.get(clave)
        if nodo is None:
            if self._taxonomia:
                padre = self._nodos_grupo.get(_normalizar(GRUPO_OTROS))
                if padre is None:
                    padre = arbol.agregar(arbol.raiz, GRUPO_OTROS)
                    self._nodos_grupo[_normalizar(GRUPO_OTROS)] = padre
            else:
                padre = arbol.raiz
            etiqueta = lugar.categoria.strip().capitalize() or "Sin categoría"
            nodo = arbol.agregar(padre, etiqueta)
            self._nodos_categoria[clave] = nodo
        arbol.agregar(nodo, lugar.nombre, valor=lugar)

    @property
    def arbol_categorias(self):
        """El árbol general: raíz > grupos > categorías > lugares (hojas)."""
        return self._arbol_categorias

    def buscar_nodo(self, texto):
        """Nodo (grupo, categoría o lugar) con ese nombre exacto, o None.

        Recorre por niveles: si un lugar se llamara igual que una categoría,
        gana la categoría, que está más cerca de la raíz.
        """
        return self._arbol_categorias.buscar(texto)

    def buscar_nodos(self, texto):
        """Todos los nodos cuyo nombre contiene el texto, en orden de lectura."""
        return self._arbol_categorias.buscar_todos(texto)

    def ruta_de(self, nodo):
        """'Dónde vamos > Para comer > Parrilla': el camino desde la raíz."""
        camino = self._arbol_categorias.camino(nodo)
        return SEPARADOR_RUTA.join(n.etiqueta for n in camino)

    def lugares_de(self, nodo):
        """Todos los lugares que cuelgan de ese nodo, a cualquier profundidad.

        Esto es lo que la lista plana no puede decir: `filtrar` responde por
        una categoría, el árbol responde también por un grupo entero.
        """
        return [
            hoja.valor
            for hoja in self._arbol_categorias.hojas(nodo)
            if hoja.valor is not None
        ]

    def lugares_de_rama(self, texto):
        """Los lugares de un grupo o categoría por nombre. None si no existe."""
        nodo = self.buscar_nodo(texto)
        if nodo is None:
            return None
        return self.lugares_de(nodo)

    def describir_nodo(self, nodo):
        """Texto corto para mostrar un nodo: cuántos lugares tiene o su puntuación."""
        if nodo.valor is not None:
            return f"{nodo.etiqueta} (⭐ {nodo.valor.puntuacion})"
        cantidad = len(self.lugares_de(nodo))
        unidad = "lugar" if cantidad == 1 else "lugares"
        return f"{nodo.etiqueta} ({cantidad} {unidad})"

    def explorar_categorias(self, incluir_lugares=False):
        """El árbol como líneas de texto. Por defecto solo grupos y categorías."""
        max_nivel = None if incluir_lugares else self._nivel_de_categorias()
        return self._arbol_categorias.dibujar(
            max_nivel=max_nivel, formato=self.describir_nodo
        )

    def recorrer_categorias(self, orden, desde=None):
        """Etiquetas de grupos y categorías en 'preorden', 'postorden' o 'niveles'.

        Los lugares no se incluyen: son las hojas y se piden con `lugares_de`.
        `desde` es el nodo desde el que se recorre (por defecto, la raíz).
        """
        recorridos = {
            "preorden": self._arbol_categorias.preorden,
            "postorden": self._arbol_categorias.postorden,
            "niveles": self._arbol_categorias.por_niveles,
        }
        if orden not in recorridos:
            raise ValueError(f"recorrido desconocido: {orden!r}")
        return [
            nodo.etiqueta for nodo in recorridos[orden](desde)
            if nodo.valor is None
        ]

    def _nivel_de_categorias(self):
        """Último nivel del árbol que todavía tiene grupos o categorías."""
        ultimo = 1
        for numero, nodos in enumerate(self._arbol_categorias.niveles(), start=1):
            if any(nodo.valor is None for nodo in nodos):
                ultimo = numero
        return ultimo

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

    def obtener_top_n(self, n=5, clave_prioridad=None):
        if n <= 0:
            return []
        heap = HeapBinario(es_max=True)
        for lugar in self._lugares:
            if clave_prioridad is None:
                prioridad = getattr(lugar, 'puntuacion', 0)
            else:
                prioridad = clave_prioridad(lugar)
            try:
                pval = float(prioridad)
            except Exception:
                pval = 0
            heap.insertar(_ItemPrioridad(pval, _normalizar(lugar.nombre), lugar))
        items = heap.top_n(n)
        return [it.elemento for it in items]



