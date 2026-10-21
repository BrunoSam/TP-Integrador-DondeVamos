"""Árbol general (n-ario) genérico (TP5).

A diferencia del BST y del AVL, acá no hay una relación de orden entre hermanos:
un nodo puede tener cualquier cantidad de hijos y el árbol representa una
**jerarquía** (Películas > Ciencia ficción > Cyberpunk), no un índice de
búsqueda. Por eso no se busca "por comparación" sino recorriendo.

La etiqueta de cada nodo es lo que se muestra y lo que se busca. La función
`clave` se inyecta como `callable` (igual que en `arbol_binario.py`) y define
cuándo dos etiquetas "son la misma": el catálogo le pasa `_normalizar` para que
"ciencia ficcion" encuentre "Ciencia ficción". Así el árbol no depende del dominio.

Todas las operaciones son iterativas, igual que en el BST del TP3: una jerarquía
cargada como cadena de n niveles reventaría el límite de recursión de Python.
"""


class NodoGeneral:
    """Nodo del árbol: una etiqueta, un valor opcional, su padre y sus hijos.

    El valor es lo que cuelga del nodo (en el catálogo, un `Lugar` en las hojas
    y `None` en las categorías). El padre se guarda en el nodo para poder subir
    hasta la raíz (ruta, nivel) sin recorrer todo el árbol.
    """

    def __init__(self, etiqueta, valor=None):
        self._etiqueta = etiqueta
        self._valor = valor
        self._padre = None
        self._hijos = []

    @property
    def etiqueta(self):
        return self._etiqueta

    @property
    def valor(self):
        return self._valor

    @property
    def padre(self):
        return self._padre

    @property
    def hijos(self):
        """Los hijos en orden de alta. Es una tupla: no se modifica desde afuera."""
        return tuple(self._hijos)

    @property
    def grado(self):
        """Cantidad de hijos directos."""
        return len(self._hijos)

    @property
    def es_hoja(self):
        return not self._hijos

    def _agregar_hijo(self, hijo):
        hijo._padre = self
        self._hijos.append(hijo)

    def _quitar_hijo(self, hijo):
        self._hijos.remove(hijo)
        hijo._padre = None

    def __repr__(self):
        return f"NodoGeneral({self._etiqueta!r}, hijos={len(self._hijos)})"


class ArbolGeneral:
    """Árbol general con raíz única.

    Invariante: todo nodo, salvo la raíz, tiene exactamente un padre, y siguiendo
    los padres siempre se llega a la raíz (no hay ciclos ni nodos sueltos).

    Los niveles se cuentan desde 1, igual que `altura()` en los otros árboles:
    la raíz está en el nivel 1 y `altura()` es el mayor nivel que existe.
    """

    def __init__(self, etiqueta_raiz, valor=None, clave=None):
        self._clave_de = clave if clave is not None else (lambda etiqueta: etiqueta)
        self._raiz = NodoGeneral(etiqueta_raiz, valor)
        self._cantidad = 1

    @property
    def raiz(self):
        return self._raiz

    # --- Alta y baja --------------------------------------------------------

    def agregar(self, padre, etiqueta, valor=None):
        """Cuelga un hijo nuevo del nodo `padre` y lo devuelve. O(h).

        El costo es el de comprobar que `padre` pertenece a este árbol (subir
        hasta la raíz); el alta en sí es O(1). Se permiten hermanos con la misma
        etiqueta: en el catálogo puede haber dos lugares con el mismo nombre.
        """
        if not self._pertenece(padre):
            raise ValueError("el nodo padre no pertenece a este árbol")
        nuevo = NodoGeneral(etiqueta, valor)
        padre._agregar_hijo(nuevo)
        self._cantidad += 1
        return nuevo

    def eliminar(self, nodo):
        """Elimina el nodo y todo su subárbol. Devuelve cuántos nodos se fueron.

        La raíz no se puede eliminar: sin raíz no hay árbol.
        """
        if not self._pertenece(nodo):
            raise ValueError("el nodo no pertenece a este árbol")
        if nodo is self._raiz:
            raise ValueError("no se puede eliminar la raíz")
        removidos = len(self.preorden(nodo))
        nodo.padre._quitar_hijo(nodo)
        self._cantidad -= removidos
        return removidos

    # --- Búsquedas ----------------------------------------------------------

    def buscar(self, texto, desde=None):
        """Primer nodo cuya etiqueta coincide con `texto`, o None. O(n).

        Recorre **por niveles** (BFS), así que devuelve el match más cercano a
        `desde` (por defecto, la raíz). Si hay dos etiquetas iguales a distinta
        profundidad, gana la menos profunda.
        """
        clave = self._clave_de(texto)
        for nodo in self.por_niveles(desde):
            if self._clave_de(nodo.etiqueta) == clave:
                return nodo
        return None

    def buscar_profundidad(self, texto, desde=None):
        """Igual que `buscar`, pero recorriendo en preorden (DFS).

        Devuelve el primer match en orden de lectura, que puede ser más profundo
        que el de `buscar` si la etiqueta se repite.
        """
        clave = self._clave_de(texto)
        for nodo in self.preorden(desde):
            if self._clave_de(nodo.etiqueta) == clave:
                return nodo
        return None

    def buscar_todos(self, texto, desde=None):
        """Todos los nodos cuya etiqueta CONTIENE `texto`, en preorden. O(n).

        Requiere que `clave` devuelva `str`, porque compara por inclusión.
        """
        clave = self._clave_de(texto)
        return [
            nodo for nodo in self.preorden(desde)
            if clave in self._clave_de(nodo.etiqueta)
        ]

    def contiene(self, texto):
        """True si hay algún nodo con esa etiqueta. O(n)."""
        return self.buscar(texto) is not None

    # --- Posición de un nodo ------------------------------------------------

    def camino(self, nodo):
        """Lista de nodos desde la raíz hasta `nodo` (ambos incluidos). O(h)."""
        recorrido = []
        actual = nodo
        while actual is not None:
            recorrido.append(actual)
            actual = actual.padre
        if not recorrido or recorrido[-1] is not self._raiz:
            raise ValueError("el nodo no pertenece a este árbol")
        recorrido.reverse()
        return recorrido

    def nivel(self, nodo):
        """Nivel del nodo: la raíz es 1. O(h)."""
        return len(self.camino(nodo))

    # --- Recorridos ---------------------------------------------------------
    # Todos devuelven listas de NODOS y aceptan `desde` para recorrer solo un
    # subárbol (por defecto, el árbol entero).

    def preorden(self, desde=None):
        """Padre antes que sus hijos: se lee como un índice, de arriba hacia abajo."""
        inicio = self._resolver(desde)
        resultado = []
        pila = [inicio]
        while pila:
            nodo = pila.pop()
            resultado.append(nodo)
            # Se apilan al revés para que el primer hijo salga primero.
            pila.extend(reversed(nodo._hijos))
        return resultado

    def postorden(self, desde=None):
        """Hijos antes que su padre: primero lo más específico, la raíz al final."""
        inicio = self._resolver(desde)
        orden_inverso = []
        pila = [inicio]
        while pila:
            nodo = pila.pop()
            orden_inverso.append(nodo)
            pila.extend(nodo._hijos)
        orden_inverso.reverse()
        return orden_inverso

    def niveles(self, desde=None):
        """Los nodos agrupados por nivel: una lista por cada nivel (BFS)."""
        inicio = self._resolver(desde)
        resultado = []
        actual = [inicio]
        while actual:
            resultado.append(actual)
            siguiente = []
            for nodo in actual:
                siguiente.extend(nodo._hijos)
            actual = siguiente
        return resultado

    def por_niveles(self, desde=None):
        """Recorrido por niveles (BFS): de lo general a lo específico."""
        return [nodo for nivel in self.niveles(desde) for nodo in nivel]

    def hojas(self, desde=None):
        """Los nodos sin hijos, en preorden."""
        return [nodo for nodo in self.preorden(desde) if nodo.es_hoja]

    # --- Medidas ------------------------------------------------------------

    def altura(self):
        """Niveles del camino más largo. Un árbol con solo la raíz tiene altura 1."""
        return len(self.niveles())

    def tamano(self):
        return self._cantidad

    # --- Presentación -------------------------------------------------------

    def dibujar(self, desde=None, max_nivel=None, formato=None):
        """El árbol como líneas de texto con ramas (├── └── │), listo para imprimir.

        `max_nivel` limita cuántos niveles se muestran contando desde `desde`
        (1 = solo ese nodo). `formato` es un `callable(nodo) -> str`; por defecto
        se imprime la etiqueta.
        """
        inicio = self._resolver(desde)
        formatear = formato if formato is not None else (lambda n: n.etiqueta)
        lineas = [formatear(inicio)]
        if max_nivel is not None and max_nivel <= 1:
            return lineas

        pila = []
        self._apilar_hijos(pila, inicio, "", 2)
        while pila:
            nodo, prefijo, es_ultimo, nivel = pila.pop()
            lineas.append(prefijo + ("└── " if es_ultimo else "├── ") + formatear(nodo))
            if max_nivel is not None and nivel >= max_nivel:
                continue
            self._apilar_hijos(
                pila, nodo, prefijo + ("    " if es_ultimo else "│   "), nivel + 1
            )
        return lineas

    @staticmethod
    def _apilar_hijos(pila, nodo, prefijo, nivel):
        hijos = nodo._hijos
        for i in range(len(hijos) - 1, -1, -1):
            pila.append((hijos[i], prefijo, i == len(hijos) - 1, nivel))

    # --- Internos -----------------------------------------------------------

    def _pertenece(self, nodo):
        while nodo is not None:
            if nodo is self._raiz:
                return True
            nodo = nodo.padre
        return False

    def _resolver(self, desde):
        """El nodo desde el que se recorre: la raíz si no se indica otro."""
        if desde is None:
            return self._raiz
        if not self._pertenece(desde):
            raise ValueError("el nodo no pertenece a este árbol")
        return desde

    def __contains__(self, texto):
        return self.contiene(texto)

    def __len__(self):
        return self._cantidad

    def __repr__(self):
        return (
            f"ArbolGeneral(raiz={self._raiz.etiqueta!r}, "
            f"tamano={self._cantidad}, altura={self.altura()})"
        )
