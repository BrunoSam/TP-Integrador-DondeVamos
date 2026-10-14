"""Árbol AVL genérico (TP4).

Extiende el BST del TP3 con rebalanceo por rotaciones, de modo que la altura
queda garantizada en O(log n) sin importar el orden en que lleguen las claves.

La clave se inyecta como `callable`, igual que en `arbol_binario.py`, así el
árbol no depende del dominio.

Sobre la recursión: el BST del TP3 es iterativo **a propósito**, porque un árbol
sin balancear con claves ordenadas alcanza altura n y una versión recursiva
revienta con el límite de recursión de Python (1000). En un AVL ese problema
desaparece por construcción: la altura nunca supera 1,44·log₂(n+2), o sea ~25
niveles para 100.000 claves. Por eso acá la inserción puede ser recursiva sin
riesgo, y el contraste con el TP3 queda a la vista.
"""


class NodoAVL:
    """Nodo del AVL: clave, valor, hijos y la altura de su subárbol.

    La altura es un dato del nodo (no se recalcula recorriendo el subárbol en
    cada consulta): al rotar se actualiza en O(1).
    """

    def __init__(self, clave, valor):
        self._clave = clave
        self._valor = valor
        self._izquierdo = None
        self._derecho = None
        self._altura = 1

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

    @property
    def altura(self):
        return self._altura

    def _reemplazar_valor(self, valor):
        """Cambia el valor conservando la clave (clave duplicada)."""
        self._valor = valor

    def __repr__(self):
        return f"NodoAVL({self._clave!r}, altura={self._altura})"


class ArbolAVL:
    """Árbol AVL: BST que se mantiene balanceado con rotaciones.

    Invariante doble:
      1. De búsqueda: subárbol izquierdo < nodo < subárbol derecho.
      2. De balance: para todo nodo, |altura(izq) - altura(der)| <= 1.

    El invariante 2 es lo que garantiza altura O(log n) y, con ella, búsqueda e
    inserción en O(log n) en el **peor caso**, no solo en promedio.

    La API pública es la misma que la de `ArbolBinarioBusqueda`, así que es un
    reemplazo directo ("drop-in").
    """

    def __init__(self, clave=None):
        self._clave_de = clave if clave is not None else (lambda valor: valor)
        self._raiz = None
        self._cantidad = 0

    @property
    def raiz(self):
        return self._raiz

    def insertar(self, valor):
        """Inserta un valor, rebalanceando. True si se agregó, False si la clave
        ya existía (en ese caso actualiza el valor, como el BST del TP3)."""
        clave = self._clave_de(valor)
        self._raiz, agrego = self._insertar(self._raiz, clave, valor)
        if agrego:
            self._cantidad += 1
        return agrego

    def _insertar(self, nodo, clave, valor):
        """Inserta recursivo y devuelve `(nodo_raiz, agrego)`.

        La recursión baja por el camino de búsqueda (a lo sumo O(log n) niveles)
        y, al volver, actualiza alturas y aplica la rotación que haga falta.
        """
        if nodo is None:
            return NodoAVL(clave, valor), True

        if clave == nodo.clave:
            nodo._reemplazar_valor(valor)
            return nodo, False

        if clave < nodo.clave:
            nodo._izquierdo, agrego = self._insertar(nodo.izquierdo, clave, valor)
        else:
            nodo._derecho, agrego = self._insertar(nodo.derecho, clave, valor)

        if not agrego:
            return nodo, False

        return self._rebalancear(nodo), True

    def buscar(self, clave):
        """Devuelve el valor con esa clave, o None. O(log n) garantizado.

        La clave llega ya normalizada: la función `clave` solo se aplica al
        insertar, igual que en el BST del TP3.
        """
        nodo = self._raiz
        while nodo is not None:
            if clave == nodo.clave:
                return nodo.valor
            nodo = nodo.izquierdo if clave < nodo.clave else nodo.derecho
        return None

    def contiene(self, clave):
        """True si la clave está en el árbol. O(log n) garantizado."""
        nodo = self._raiz
        while nodo is not None:
            if clave == nodo.clave:
                return True
            nodo = nodo.izquierdo if clave < nodo.clave else nodo.derecho
        return False

    # --- Balanceo -----------------------------------------------------------

    def factor_balance(self, nodo):
        """altura(izq) - altura(der). Entre -1 y 1 si el nodo está balanceado.

        Positivo = pesa la izquierda; negativo = pesa la derecha.
        """
        if nodo is None:
            return 0
        return (
            self._altura_de(nodo.izquierdo) - self._altura_de(nodo.derecho)
        )

    def esta_balanceado(self):
        """True si TODOS los nodos respetan |factor de balance| <= 1."""
        if self._raiz is None:
            return True
        pila = [self._raiz]
        while pila:
            nodo = pila.pop()
            if abs(self.factor_balance(nodo)) > 1:
                return False
            if nodo.izquierdo is not None:
                pila.append(nodo.izquierdo)
            if nodo.derecho is not None:
                pila.append(nodo.derecho)
        return True

    def _rebalancear(self, nodo):
        """Recalcula la altura del nodo y aplica la rotación si quedó desbalanceado."""
        self._actualizar_altura(nodo)
        factor = self.factor_balance(nodo)

        # Izquierda pesada.
        if factor > 1:
            if self.factor_balance(nodo.izquierdo) < 0:
                # Caso izquierda-derecha: primero una rotación simple.
                nodo._izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)

        # Derecha pesada.
        if factor < -1:
            if self.factor_balance(nodo.derecho) > 0:
                # Caso derecha-izquierda: primero una rotación simple.
                nodo._derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)

        return nodo

    def _rotar_derecha(self, y):
        """Rotación simple a la derecha (caso izquierda-izquierda)."""
        x = y.izquierdo
        traslado = x.derecho
        x._derecho = y
        y._izquierdo = traslado
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x):
        """Rotación simple a la izquierda (caso derecha-derecha)."""
        y = x.derecho
        traslado = y.izquierdo
        y._izquierdo = x
        x._derecho = traslado
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _actualizar_altura(self, nodo):
        nodo._altura = 1 + max(
            self._altura_de(nodo.izquierdo), self._altura_de(nodo.derecho)
        )

    @staticmethod
    def _altura_de(nodo):
        return nodo.altura if nodo is not None else 0

    # --- Recorridos y medidas (misma API que el BST) ------------------------

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
        """Niveles del camino más largo. Un árbol vacío tiene altura 0.

        Se lee de la raíz en O(1): las rotaciones mantienen `_altura` al día.
        """
        return self._altura_de(self._raiz)

    def tamano(self):
        return self._cantidad

    def __contains__(self, clave):
        return self.contiene(clave)

    def __len__(self):
        return self._cantidad

    def __bool__(self):
        return self._raiz is not None

    def __repr__(self):
        return (
            f"ArbolAVL(tamano={self._cantidad}, altura={self.altura()}, "
            f"balanceado={self.esta_balanceado()})"
        )
