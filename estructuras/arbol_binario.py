"""Árbol binario de búsqueda genérico (TP3).

La clave se inyecta como `callable`, así el árbol no depende del dominio.
Todas las operaciones son iterativas.
"""


class NodoArbol:
    """Nodo del árbol: una clave comparable, un valor y sus dos hijos."""

    def __init__(self, clave, valor):
        self._clave = clave
        self._valor = valor
        self._izquierdo = None
        self._derecho = None

    @property
    def clave(self):
        return self._clave

    @property
    def valor(self):
        return self._valor

    @property
    def izquierdo(self):
        return self._izquierdo

    @property
    def derecho(self):
        return self._derecho

    def _reemplazar_valor(self, valor):
        """Cambia el valor conservando la clave (clave duplicada)."""
        self._valor = valor

    def __repr__(self):
        return f"NodoArbol({self._clave!r})"


class ArbolBinarioBusqueda:
    """BST genérico: inserción, búsqueda y recorridos en orden.

    Invariante: todo nodo del subárbol izquierdo tiene clave menor que la del
    nodo, y todo nodo del subárbol derecho tiene clave mayor.
    """

    def __init__(self, clave=None):
        self._clave_de = clave if clave is not None else (lambda valor: valor)
        self._raiz = None
        self._cantidad = 0

    @property
    def raiz(self):
        return self._raiz

    def insertar(self, valor):
        """Inserta un valor. True si se agregó, False si la clave ya existía."""
        clave = self._clave_de(valor)
        nuevo = NodoArbol(clave, valor)

        if self._raiz is None:
            self._raiz = nuevo
            self._cantidad += 1
            return True

        nodo = self._raiz
        while True:
            if clave == nodo.clave:
                nodo._reemplazar_valor(valor)
                return False
            if clave < nodo.clave:
                if nodo.izquierdo is None:
                    nodo._izquierdo = nuevo
                    self._cantidad += 1
                    return True
                nodo = nodo.izquierdo
            else:
                if nodo.derecho is None:
                    nodo._derecho = nuevo
                    self._cantidad += 1
                    return True
                nodo = nodo.derecho

    def buscar(self, clave):
        """Devuelve el valor con esa clave, o None si no está. O(log n).

        La clave llega ya normalizada: la función `clave` solo se aplica al
        insertar.
        """
        nodo = self._raiz
        while nodo is not None:
            if clave == nodo.clave:
                return nodo.valor
            nodo = nodo.izquierdo if clave < nodo.clave else nodo.derecho
        return None

    def contiene(self, clave):
        """True si la clave está en el árbol. O(log n)."""
        nodo = self._raiz
        while nodo is not None:
            if clave == nodo.clave:
                return True
            nodo = nodo.izquierdo if clave < nodo.clave else nodo.derecho
        return False

    def inorder(self):
        """Recorrido en orden (izq, nodo, der): los valores, ya ordenados."""
        resultado = []
        pila = []
        nodo = self._raiz
        while pila or nodo is not None:
            while nodo is not None:
                pila.append(nodo)
                nodo = nodo.izquierdo
            nodo = pila.pop()
            resultado.append(nodo.valor)
            nodo = nodo.derecho
        return resultado

    def preorder(self):
        """Recorrido preorden (nodo, izq, der): los valores, raíz primero."""
        resultado = []
        if self._raiz is None:
            return resultado
        pila = [self._raiz]
        while pila:
            nodo = pila.pop()
            resultado.append(nodo.valor)
            if nodo.derecho is not None:
                pila.append(nodo.derecho)
            if nodo.izquierdo is not None:
                pila.append(nodo.izquierdo)
        return resultado

    def postorder(self):
        """Recorrido postorden (izq, der, nodo): los valores, raíz al final."""
        if self._raiz is None:
            return []
        visiting = [self._raiz]
        orden_inverso = []
        while visiting:
            nodo = visiting.pop()
            orden_inverso.append(nodo.valor)
            if nodo.izquierdo is not None:
                visiting.append(nodo.izquierdo)
            if nodo.derecho is not None:
                visiting.append(nodo.derecho)
        orden_inverso.reverse()
        return orden_inverso

    def altura(self):
        """Niveles del camino más largo. Un árbol vacío tiene altura 0."""
        if self._raiz is None:
            return 0
        maximo = 0
        pila = [(self._raiz, 1)]
        while pila:
            nodo, nivel = pila.pop()
            if nivel > maximo:
                maximo = nivel
            if nodo.izquierdo is not None:
                pila.append((nodo.izquierdo, nivel + 1))
            if nodo.derecho is not None:
                pila.append((nodo.derecho, nivel + 1))
        return maximo

    def tamano(self):
        return self._cantidad

    def __contains__(self, clave):
        return self.contiene(clave)

    def __len__(self):
        return self._cantidad

    def __bool__(self):
        return self._raiz is not None

    def __repr__(self):
        return f"ArbolBinarioBusqueda(tamano={self._cantidad}, altura={self.altura()})"
