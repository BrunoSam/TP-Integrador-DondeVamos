import unittest

from estructuras.arbol_binario import ArbolBinarioBusqueda
from servicios.catalogo import _normalizar


def _arbol_de(valores, clave=None):
    arbol = ArbolBinarioBusqueda(clave=clave)
    for valor in valores:
        arbol.insertar(valor)
    return arbol


def _arbol_completo(n):
    """Inserta 1..n siempre por el medio: da un árbol completo balanceado."""
    arbol = ArbolBinarioBusqueda()

    def agregar(lo, hi):
        if lo > hi:
            return
        medio = (lo + hi) // 2
        arbol.insertar(medio)
        agregar(lo, medio - 1)
        agregar(medio + 1, hi)

    agregar(1, n)
    return arbol


class TestInsercion(unittest.TestCase):

    def test_insertar_en_arbol_vacio_devuelve_true(self):
        arbol = ArbolBinarioBusqueda()
        self.assertTrue(arbol.insertar(5))
        self.assertEqual(len(arbol), 1)

    def test_raiz_es_el_primero_insertado(self):
        arbol = _arbol_de([50, 30, 70])
        self.assertEqual(arbol.raiz.valor, 50)

    def test_inserta_izquierda_y_derecha_segun_la_clave(self):
        arbol = _arbol_de([50, 30, 70, 20, 40])
        self.assertEqual(arbol.raiz.izquierdo.valor, 30)
        self.assertEqual(arbol.raiz.derecho.valor, 70)
        self.assertEqual(arbol.raiz.izquierdo.izquierdo.valor, 20)
        self.assertEqual(arbol.raiz.izquierdo.derecho.valor, 40)

    def test_clave_duplicada_no_crea_nodo_ni_cambia_el_tamano(self):
        arbol = _arbol_de([5, 3, 8])
        self.assertFalse(arbol.insertar(5))
        self.assertEqual(len(arbol), 3)

    def test_clave_duplicada_actualiza_el_valor(self):
        arbol = ArbolBinarioBusqueda(clave=lambda x: x[0])
        arbol.insertar(("a", 1))
        arbol.insertar(("b", 2))
        arbol.insertar(("a", 99))
        self.assertEqual(len(arbol), 2)
        self.assertEqual(arbol.buscar("a"), ("a", 99))


class TestBusqueda(unittest.TestCase):

    def test_encuentra_la_raiz(self):
        arbol = _arbol_de([50, 30, 70])
        self.assertEqual(arbol.buscar(50), 50)

    def test_encuentra_un_nodo_interior(self):
        arbol = _arbol_de([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(arbol.buscar(40), 40)

    def test_devuelve_none_si_no_existe(self):
        arbol = _arbol_de([50, 30, 70])
        self.assertIsNone(arbol.buscar(99))

    def test_buscar_en_arbol_vacio_devuelve_none(self):
        self.assertIsNone(ArbolBinarioBusqueda().buscar(1))

    def test_contiene_es_consistente_con_buscar(self):
        arbol = _arbol_de([50, 30, 70])
        self.assertTrue(arbol.contiene(30))
        self.assertFalse(arbol.contiene(31))
        self.assertIn(70, arbol)
        self.assertNotIn(31, arbol)

    def test_devuelve_el_valor_y_no_la_clave(self):
        arbol = ArbolBinarioBusqueda(clave=lambda par: par[0])
        arbol.insertar(("La Biela", 1))
        self.assertEqual(arbol.buscar("La Biela"), ("La Biela", 1))

    def test_es_insensible_a_mayusculas_y_acentos(self):
        """`buscar` recibe la clave ya normalizada, como en el catálogo."""
        arbol = ArbolBinarioBusqueda(clave=_normalizar)
        arbol.insertar("Gastronomía del Sur")
        clave = _normalizar("GASTRONOMIA DEL SUR")
        self.assertEqual(clave, "gastronomia del sur")
        self.assertEqual(arbol.buscar(clave), "Gastronomía del Sur")


class TestRecorridos(unittest.TestCase):

    def test_inorder_devuelve_los_valores_ordenados(self):
        arbol = _arbol_de([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(arbol.inorder(), [20, 30, 40, 50, 60, 70, 80])

    def test_inorder_es_igual_a_sorted_para_cualquier_orden_de_insercion(self):
        valores = [42, 7, 91, 33, 15, 88, 54, 3, 67, 21]
        self.assertEqual(_arbol_de(valores).inorder(), sorted(valores))

    def test_preorder_deja_la_raiz_primero(self):
        arbol = _arbol_de([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(arbol.preorder(), [50, 30, 20, 40, 70, 60, 80])

    def test_postorder_deja_la_raiz_al_final(self):
        arbol = _arbol_de([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(arbol.postorder(), [20, 40, 30, 60, 80, 70, 50])

    def test_postorder_de_un_nodo_sin_derecho_no_omite_izquierdo(self):
        """Regresión: la raíz sin hijo derecho tiene que recorrer igual su
        subárbol izquierdo."""
        arbol = _arbol_de([2, 1])
        self.assertEqual(arbol.postorder(), [1, 2])

    def test_postorder_conserva_todos_los_valores_para_cualquier_forma(self):
        """El postorden tiene que devolver los n nodos siempre, no solo cuando
        el árbol queda balanceado."""
        for n in range(1, 40):
            for raiz in range(n):
                for hijo in range(n):
                    if raiz == hijo:
                        continue
                    with self.subTest(n=n, raiz=raiz, hijo=hijo):
                        arbol = _arbol_de([raiz, hijo])
                        self.assertEqual(arbol.postorder(), [hijo, raiz])
        for orden in ([42, 7, 91, 33, 15, 88, 54, 3, 67, 21],
                      list(range(50)),
                      sorted([42, 7, 91, 33, 15, 88, 54, 3, 67, 21])):
            with self.subTest(orden=orden[:3]):
                arbol = _arbol_de(orden)
                self.assertEqual(sorted(arbol.postorder()), sorted(orden))

    def test_los_recorridos_conservan_el_conjunto_de_valores(self):
        valores = [42, 7, 91, 33, 15, 88, 54, 3, 67, 21]
        arbol = _arbol_de(valores)
        for recorrido in (arbol.inorder(), arbol.preorder(), arbol.postorder()):
            self.assertEqual(sorted(recorrido), sorted(valores))

    def test_solo_inorder_es_invariante_al_orden_de_insercion(self):
        """El orden de inserción cambia la FORMA del árbol, así que preorder y
        postorder NO son invariantes: lo único garantizado es que inorder
        devuelve siempre las claves ordenadas."""
        a = _arbol_de([42, 7, 91])
        b = _arbol_de([7, 42, 91])
        self.assertEqual(a.inorder(), b.inorder())
        self.assertNotEqual(a.preorder(), b.preorder())
        self.assertNotEqual(a.postorder(), b.postorder())

    def test_preorder_empieza_en_la_raiz_y_postorder_termina_en_la_raiz(self):
        for orden in ([42, 7, 91], [7, 42, 91], [91, 7, 42], [7, 91, 42]):
            arbol = _arbol_de(orden)
            self.assertEqual(arbol.preorder()[0], arbol.raiz.valor)
            self.assertEqual(arbol.postorder()[-1], arbol.raiz.valor)

    def test_recorridos_en_arbol_vacio_devuelven_lista_vacia(self):
        arbol = ArbolBinarioBusqueda()
        self.assertEqual(arbol.inorder(), [])
        self.assertEqual(arbol.preorder(), [])
        self.assertEqual(arbol.postorder(), [])

    def test_arbol_de_un_solo_nodo(self):
        arbol = _arbol_de([7])
        self.assertEqual(arbol.inorder(), [7])
        self.assertEqual(arbol.preorder(), [7])
        self.assertEqual(arbol.postorder(), [7])


class TestAlturaYTamano(unittest.TestCase):

    def test_altura_de_arbol_vacio_es_cero(self):
        self.assertEqual(ArbolBinarioBusqueda().altura(), 0)

    def test_altura_de_un_solo_nodo_es_uno(self):
        self.assertEqual(_arbol_de([1]).altura(), 1)

    def test_altura_de_arbol_completo_es_log2_de_n_mas_uno(self):
        # 31 nodos Full = 2^5 - 1 -> 5 niveles, insertando siempre por el medio
        self.assertEqual(_arbol_completo(31).altura(), 5)
        self.assertEqual(_arbol_completo(1).altura(), 1)
        self.assertEqual(_arbol_completo(1023).altura(), 10)

    def test_altura_de_insercion_ordenada_es_n(self):
        n = 8
        self.assertEqual(_arbol_de(list(range(n))).altura(), n)

    def test_tamano_cuenta_los_valores_insertados(self):
        arbol = _arbol_de([5, 3, 8, 1])
        self.assertEqual(arbol.tamano(), 4)
        self.assertEqual(len(arbol), 4)

    def test_bool_es_falso_solo_si_esta_vacio(self):
        self.assertFalse(ArbolBinarioBusqueda())
        arbol = ArbolBinarioBusqueda()
        self.assertFalse(arbol)
        arbol.insertar(1)
        self.assertTrue(arbol)

    def test_altura_no_revienta_con_orden_de_insercion_peor(self):
        arbol = _arbol_de(list(range(2000)))
        self.assertEqual(arbol.altura(), 2000)
        self.assertIsNotNone(arbol.buscar(1999))


if __name__ == "__main__":
    unittest.main()
