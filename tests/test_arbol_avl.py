import math
import random
import unittest

from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_binario import ArbolBinarioBusqueda
from servicios.catalogo import _normalizar


def _arbol_de(valores, clave=None):
    arbol = ArbolAVL(clave=clave)
    for valor in valores:
        arbol.insertar(valor)
    return arbol


def _altura_maxima_teorica(n):
    """Cota superior de la altura de un AVL con n nodos: 1,44·log₂(n+2)."""
    if n == 0:
        return 0
    return math.ceil(1.4405 * math.log2(n + 2) - 0.3277)


class TestRotaciones(unittest.TestCase):
    """Cada rotación tiene un caso mínimo de 3 claves con raíz 20."""

    def test_caso_izquierda_izquierda_rota_a_derecha(self):
        arbol = _arbol_de([30, 20, 10])
        self.assertEqual(arbol.raiz.valor, 20)
        self.assertEqual(arbol.raiz.izquierdo.valor, 10)
        self.assertEqual(arbol.raiz.derecho.valor, 30)
        self.assertEqual(arbol.altura(), 2)

    def test_caso_derecha_derecha_rota_a_izquierda(self):
        arbol = _arbol_de([10, 20, 30])
        self.assertEqual(arbol.raiz.valor, 20)
        self.assertEqual(arbol.raiz.izquierdo.valor, 10)
        self.assertEqual(arbol.raiz.derecho.valor, 30)
        self.assertEqual(arbol.altura(), 2)

    def test_caso_izquierda_derecha_rota_doble(self):
        arbol = _arbol_de([30, 10, 20])
        self.assertEqual(arbol.raiz.valor, 20)
        self.assertEqual(arbol.raiz.izquierdo.valor, 10)
        self.assertEqual(arbol.raiz.derecho.valor, 30)
        self.assertEqual(arbol.altura(), 2)

    def test_caso_derecha_izquierda_rota_doble(self):
        arbol = _arbol_de([10, 30, 20])
        self.assertEqual(arbol.raiz.valor, 20)
        self.assertEqual(arbol.raiz.izquierdo.valor, 10)
        self.assertEqual(arbol.raiz.derecho.valor, 30)
        self.assertEqual(arbol.altura(), 2)

    def test_rotacion_simple_conserva_el_valor_de_la_clave_duplicada(self):
        arbol = _arbol_de([30, 20, 10, 20])
        self.assertEqual(len(arbol), 3)
        self.assertTrue(arbol.esta_balanceado())


class TestInvarianteDeBalance(unittest.TestCase):

    def _claves(self, valores):
        return sorted(v for v in valores)

    def test_un_solo_nodo_esta_balanceado(self):
        arbol = _arbol_de([1])
        self.assertTrue(arbol.esta_balanceado())
        self.assertEqual(arbol.altura(), 1)

    def test_arbol_vacio_esta_balanceado(self):
        arbol = ArbolAVL()
        self.assertTrue(arbol.esta_balanceado())
        self.assertEqual(arbol.altura(), 0)

    def test_insercion_ascendente_queda_balanceada(self):
        arbol = _arbol_de(list(range(1000)))
        self.assertTrue(arbol.esta_balanceado())
        self.assertLessEqual(arbol.altura(), _altura_maxima_teorica(1000))

    def test_insercion_descendente_queda_balanceada(self):
        arbol = _arbol_de(list(range(1000, 0, -1)))
        self.assertTrue(arbol.esta_balanceado())
        self.assertLessEqual(arbol.altura(), _altura_maxima_teorica(1000))

    def test_secuencias_aleatorias_quedan_balanceadas(self):
        random.seed(2024)
        for tamano in (10, 50, 200, 1000):
            valores = list(range(tamano))
            random.shuffle(valores)
            with self.subTest(tamano=tamano):
                arbol = _arbol_de(valores)
                self.assertTrue(arbol.esta_balanceado())
                self.assertLessEqual(arbol.altura(), _altura_maxima_teorica(tamano))

    def test_la_altura_nunca_supera_la_cota_teorica(self):
        """La propiedad que define al AVL: h <= 1,44·log₂(n+2)."""
        random.seed(7)
        for tamano in (1, 2, 3, 5, 8, 13, 21, 100, 500, 2000):
            valores = list(range(tamano))
            random.shuffle(valores)
            with self.subTest(tamano=tamano):
                arbol = _arbol_de(valores)
                self.assertLessEqual(
                    arbol.altura(), _altura_maxima_teorica(tamano)
                )

    def test_comparacion_altura_contra_el_bst_sin_balancear(self):
        """El punto del TP4: con datos ordenados el BST degenera y el AVL no."""
        n = 1000
        bst = ArbolBinarioBusqueda()
        avl = ArbolAVL()
        for valor in range(n):
            bst.insertar(valor)
            avl.insertar(valor)
        self.assertEqual(bst.altura(), n)              # lista enlazada
        self.assertLessEqual(avl.altura(), 15)          # ~log₂ n
        self.assertLess(avl.altura(), bst.altura() / 50)


class TestInsercion(unittest.TestCase):

    def test_insertar_en_arbol_vacio_devuelve_true(self):
        arbol = ArbolAVL()
        self.assertTrue(arbol.insertar(5))
        self.assertEqual(len(arbol), 1)

    def test_clave_duplicada_no_crea_nodo_ni_cambia_el_tamano(self):
        arbol = _arbol_de([5, 3, 8])
        self.assertFalse(arbol.insertar(5))
        self.assertEqual(len(arbol), 3)

    def test_clave_duplicada_actualiza_el_valor(self):
        arbol = ArbolAVL(clave=lambda x: x[0])
        arbol.insertar(("a", 1))
        arbol.insertar(("b", 2))
        arbol.insertar(("a", 99))
        self.assertEqual(len(arbol), 2)
        self.assertEqual(arbol.buscar("a"), ("a", 99))

    def test_inserta_izquierda_y_derecha_segun_la_clave(self):
        arbol = _arbol_de([50, 30, 70, 20, 40])
        self.assertEqual(arbol.raiz.valor, 50)
        self.assertEqual(arbol.raiz.izquierdo.valor, 30)
        self.assertEqual(arbol.raiz.derecho.valor, 70)


class TestBusqueda(unittest.TestCase):

    def test_encuentra_la_raiz(self):
        self.assertEqual(_arbol_de([50, 30, 70]).buscar(50), 50)

    def test_encuentra_un_nodo_interior(self):
        arbol = _arbol_de([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(arbol.buscar(40), 40)

    def test_devuelve_none_si_no_existe(self):
        self.assertIsNone(_arbol_de([50, 30, 70]).buscar(99))

    def test_buscar_en_arbol_vacio_devuelve_none(self):
        self.assertIsNone(ArbolAVL().buscar(1))

    def test_contiene_es_consistente_con_buscar(self):
        arbol = _arbol_de([50, 30, 70])
        self.assertTrue(arbol.contiene(30))
        self.assertFalse(arbol.contiene(31))
        self.assertIn(70, arbol)
        self.assertNotIn(31, arbol)

    def test_todas_las_claves_siguen_siendo_encontrables(self):
        """El rebalanceo no pierde nodos: con 1.000 ordenadas se encuentran todas."""
        arbol = _arbol_de(list(range(1000)))
        for clave in range(1000):
            self.assertIsNotNone(arbol.buscar(clave))

    def test_devuelve_el_valor_y_no_la_clave(self):
        arbol = ArbolAVL(clave=lambda par: par[0])
        arbol.insertar(("La Biela", 1))
        self.assertEqual(arbol.buscar("La Biela"), ("La Biela", 1))

    def test_es_insensible_a_mayusculas_y_acentos(self):
        arbol = ArbolAVL(clave=_normalizar)
        arbol.insertar("Gastronomía del Sur")
        self.assertEqual(arbol.buscar(_normalizar("GASTRONOMIA DEL SUR")), "Gastronomía del Sur")


class TestRecorridos(unittest.TestCase):

    def test_inorder_devuelve_los_valores_ordenados(self):
        arbol = _arbol_de([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(arbol.inorder(), [20, 30, 40, 50, 60, 70, 80])

    def test_inorder_es_igual_a_sorted_para_cualquier_orden(self):
        random.seed(11)
        for _ in range(20):
            valores = list(range(50))
            random.shuffle(valores)
            self.assertEqual(_arbol_de(valores).inorder(), sorted(valores))

    def test_los_tres_recorridos_conservan_el_conjunto_de_valores(self):
        valores = [42, 7, 91, 33, 15, 88, 54, 3, 67, 21]
        arbol = _arbol_de(valores)
        for recorrido in (arbol.inorder(), arbol.preorder(), arbol.postorder()):
            self.assertEqual(sorted(recorrido), sorted(valores))

    def test_preorder_empieza_en_la_raiz_y_postorder_termina_en_la_raiz(self):
        arbol = _arbol_de([42, 7, 91, 33, 15])
        self.assertEqual(arbol.preorder()[0], arbol.raiz.valor)
        self.assertEqual(arbol.postorder()[-1], arbol.raiz.valor)

    def test_recorridos_en_arbol_vacio_devuelven_lista_vacia(self):
        arbol = ArbolAVL()
        self.assertEqual(arbol.inorder(), [])
        self.assertEqual(arbol.preorder(), [])
        self.assertEqual(arbol.postorder(), [])

    def test_recorridos_con_insercion_ordenada_conservan_todo(self):
        arbol = _arbol_de(list(range(100)))
        for recorrido in (arbol.inorder(), arbol.preorder(), arbol.postorder()):
            self.assertEqual(sorted(recorrido), list(range(100)))


class TestAlturaYTamano(unittest.TestCase):

    def test_altura_de_arbol_vacio_es_cero(self):
        self.assertEqual(ArbolAVL().altura(), 0)

    def test_altura_de_un_solo_nodo_es_uno(self):
        self.assertEqual(_arbol_de([1]).altura(), 1)

    def test_altura_de_tres_nodos_balanceados_es_dos(self):
        self.assertEqual(_arbol_de([2, 1, 3]).altura(), 2)

    def test_tamano_cuenta_los_valores_insertados(self):
        arbol = _arbol_de([5, 3, 8, 1])
        self.assertEqual(arbol.tamano(), 4)
        self.assertEqual(len(arbol), 4)

    def test_bool_es_falso_solo_si_esta_vacio(self):
        arbol = ArbolAVL()
        self.assertFalse(arbol)
        arbol.insertar(1)
        self.assertTrue(arbol)

    def test_una_secuencia_ordenada_no_dispara_la_recursion(self):
        """A diferencia del BST, el AVL puede ser recursivo: la altura queda
        acotada. 5.000 claves ordenadas no deben alcanzar el límite (1.000)."""
        arbol = _arbol_de(list(range(5000)))
        self.assertEqual(len(arbol), 5000)
        self.assertLess(arbol.altura(), 20)


if __name__ == "__main__":
    unittest.main()
