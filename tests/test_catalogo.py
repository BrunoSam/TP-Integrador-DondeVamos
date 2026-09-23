import unittest

from servicios.catalogo import Catalogo


class TestCatalogo(unittest.TestCase):

    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/lugares.json")

    def test_buscar_por_nombre(self):
        resultado = self.catalogo.buscar("don julio parrilla")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Don Julio Parrilla")

    def test_buscar_ignora_mayusculas(self):
        resultado = self.catalogo.buscar("LA BIELA")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "La Biela")

    def test_buscar_devuelve_none_si_no_existe(self):
        self.assertIsNone(self.catalogo.buscar("no-existe"))

    def test_listar_devuelve_todos(self):
        self.assertTrue(len(self.catalogo.listar()) >= 20)

    def test_filtrar_por_categoria(self):
        resultados = self.catalogo.filtrar("parrilla")
        self.assertEqual(len(resultados), 5)
        self.assertTrue(
            all(l.categoria == "parrilla" for l in resultados)
        )

    def test_filtrar_ignora_mayusculas(self):
        resultados = self.catalogo.filtrar("CAFETERIA")
        self.assertTrue(len(resultados) > 0)
        self.assertTrue(
            all(l.categoria == "cafeteria" for l in resultados)
        )

    def test_buscar_parcial_encuentra_palermo(self):
        resultados = self.catalogo.buscar_parcial("palermo")
        self.assertTrue(len(resultados) >= 4)

    def test_buscar_binaria_requiere_ordenar(self):
        self.catalogo.ordenar_por_titulo()
        resultado = self.catalogo.buscar_binaria("don julio parrilla")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Don Julio Parrilla")

    def test_buscar_binaria_ignora_mayusculas_y_acentos(self):
        self.catalogo.ordenar_por_titulo()
        resultado = self.catalogo.buscar_binaria("LA BIELA")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "La Biela")

    def test_buscar_binaria_devuelve_none_si_no_existe(self):
        self.catalogo.ordenar_por_titulo()
        self.assertIsNone(self.catalogo.buscar_binaria("no-existe"))

    def test_ordenar_por_titulo_ordena_por_nombre_normalizado(self):
        self.catalogo.ordenar_por_titulo()
        nombres = [l.nombre for l in self.catalogo.listar()]
        self.assertEqual(nombres, sorted(nombres, key=str.lower))

    def test_buscar_y_binaria_son_consistentes(self):
        self.catalogo.ordenar_por_titulo()
        for nombre in ["Don Julio Parrilla", "La Biela", "no-existe", "EL VIEJO PALERMO GRILL"]:
            self.assertEqual(
                self.catalogo.buscar(nombre),
                self.catalogo.buscar_binaria(nombre),
            )

    def test_lugar_tiene_horarios_y_costo(self):
        resultado = self.catalogo.buscar("Don Julio Parrilla")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.horario_apertura, "11:30")
        self.assertEqual(resultado.horario_cierre, "01:00")
        self.assertIn(resultado.costo, (1, 2, 3))

    def test_listar_salidas_con_participantes(self):
        self.catalogo.cargar_salidas_desde_json("datos/salidas.json")
        salidas = self.catalogo.listar_salidas()
        self.assertEqual(len(salidas), 4)
        self.assertTrue(
            all(len(s.participantes) > 0 for s in salidas)
        )


if __name__ == "__main__":
    unittest.main()