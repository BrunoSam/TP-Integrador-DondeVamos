import unittest
from estructuras.heap_binario import HeapBinario
from servicios.catalogo import Catalogo


class TestHeapBinario(unittest.TestCase):
    def test_insertar_y_extraer_raiz_max_heap(self):
        h = HeapBinario(es_max=True)
        for v in [5, 1, 10, 3]:
            h.insertar(v)
        self.assertEqual(h.extraer_raiz(), 10)
        self.assertEqual(h.extraer_raiz(), 5)

    def test_top_n_no_destruye(self):
        h = HeapBinario(es_max=True)
        for v in [1, 7, 3, 9]:
            h.insertar(v)
        top = h.top_n(2)
        self.assertEqual(top[0], 9)
        self.assertEqual(top[1], 7)
        self.assertEqual(h.ver_raiz(), 9)


class TestCatalogoTopN(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/lugares.json")

    def test_obtener_top_n_devuelve_n_elementos_ordenados(self):
        top = self.catalogo.obtener_top_n(5)
        self.assertEqual(len(top), 5)
        puntuaciones = [l.puntuacion for l in top]
        self.assertEqual(puntuaciones, sorted(puntuaciones, reverse=True))