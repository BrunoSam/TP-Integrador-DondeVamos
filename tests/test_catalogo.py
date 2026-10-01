import unittest

from modelos.lugar import Lugar
from modelos.salida import Salida
from servicios.catalogo import Catalogo, _normalizar


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

    def test_agregar_salida_suma_a_la_lista(self):
        self.catalogo.agregar_salida(Salida(99, "Salida de prueba", ["Ana"]))
        salidas = self.catalogo.listar_salidas()
        self.assertEqual(len(salidas), 1)
        self.assertEqual(salidas[0].nombre, "Salida de prueba")

    def test_listar_salidas_devuelve_una_copia(self):
        salidas = self.catalogo.listar_salidas()
        salidas.append(Salida(99, "No debe verse", []))
        self.assertEqual(self.catalogo.listar_salidas(), [])


class TestCatalogoArbol(unittest.TestCase):
    """Integración del BST (TP3) dentro del catálogo."""

    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/lugares.json")

    def test_el_arbol_se_construye_al_cargar(self):
        self.assertEqual(len(self.catalogo._arbol), len(self.catalogo))

    def test_buscar_arbol_encuentra_el_lugar(self):
        resultado = self.catalogo.buscar_arbol("don julio parrilla")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Don Julio Parrilla")

    def test_buscar_arbol_ignora_mayusculas_y_acentos(self):
        resultado = self.catalogo.buscar_arbol("LA BIELA")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "La Biela")

    def test_buscar_arbol_devuelve_none_si_no_existe(self):
        self.assertIsNone(self.catalogo.buscar_arbol("no-existe"))

    def test_buscar_arbol_no_requiere_ordenar_antes(self):
        """A diferencia de buscar_binaria, el árbol ya está indexado."""
        resultado = self.catalogo.buscar_arbol("El Viejo Palermo Grill")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "El Viejo Palermo Grill")

    def test_buscar_arbol_y_binaria_son_consistentes(self):
        self.catalogo.ordenar_por_titulo()
        for nombre in self._todos_los_nombres() + ["no-existe", "ZZZ", ""]:
            with self.subTest(nombre=nombre):
                self.assertEqual(
                    self.catalogo.buscar_binaria(nombre),
                    self.catalogo.buscar_arbol(nombre),
                )

    def test_buscar_arbol_y_secuencial_son_consistentes(self):
        for nombre in self._todos_los_nombres():
            with self.subTest(nombre=nombre):
                self.assertEqual(
                    self.catalogo.buscar(nombre),
                    self.catalogo.buscar_arbol(nombre),
                )

    def test_listar_ordenado_devuelve_todos_en_orden_alfabetico(self):
        ordenados = self.catalogo.listar_ordenado()
        self.assertEqual(len(ordenados), len(self.catalogo))
        nombres = [lugar.nombre for lugar in ordenados]
        self.assertEqual(nombres, sorted(nombres, key=str.lower))

    def test_listar_ordenado_es_el_inorder_del_arbol(self):
        self.assertEqual(
            [lugar.nombre for lugar in self.catalogo.listar_ordenado()],
            [lugar.nombre for lugar in self.catalogo._arbol.inorder()],
        )

    def test_listar_preorder_empieza_en_la_raiz_del_arbol(self):
        preorder = self.catalogo.listar_preorder()
        self.assertEqual(len(preorder), len(self.catalogo))
        self.assertEqual(preorder[0], self.catalogo._arbol.raiz.valor)

    def test_listar_postorder_termina_en_la_raiz_del_arbol(self):
        postorder = self.catalogo.listar_postorder()
        self.assertEqual(len(postorder), len(self.catalogo))
        self.assertEqual(postorder[-1], self.catalogo._arbol.raiz.valor)

    def test_los_tres_recorridos_conservan_los_mismos_lugares(self):
        nombres = {lugar.nombre for lugar in self.catalogo.listar()}
        for recorrido in (
            self.catalogo.listar_ordenado(),
            self.catalogo.listar_preorder(),
            self.catalogo.listar_postorder(),
        ):
            with self.subTest(recorrido=len(recorrido)):
                self.assertEqual({lugar.nombre for lugar in recorrido}, nombres)

    def test_solo_el_recorrido_en_orden_viene_alfabetico(self):
        """inorder es el único invariante al orden de inserción; preorder y
        postorder dependen de la FORMA del árbol, así que no se ordenan."""
        alfabeticos = [
            lugar.nombre for lugar in self.catalogo.listar_ordenado()
        ]
        for recorrido in (
            self.catalogo.listar_preorder(),
            self.catalogo.listar_postorder(),
        ):
            with self.subTest(recorrido=len(recorrido)):
                nombres = [lugar.nombre for lugar in recorrido]
                self.assertEqual(sorted(nombres, key=_normalizar), alfabeticos)

    def test_indexar_reconstruye_el_arbol_desde_cero(self):
        self.catalogo.indexar()
        self.assertEqual(len(self.catalogo._arbol), len(self.catalogo))
        self.assertIsNotNone(self.catalogo.buscar_arbol("La Biela"))

    def test_agregar_lugar_lo_hace_buscable_sin_reindexar(self):
        self.catalogo.agregar_lugar(Lugar(999, "El Nuevo", "Palermo", "bar", 4.0, "20:00", "02:00", 2))
        self.assertEqual(len(self.catalogo), len(self.catalogo._arbol))
        self.assertIsNotNone(self.catalogo.buscar_arbol("el nuevo"))
        self.assertEqual(len(self.catalogo.listar_preorder()), len(self.catalogo))
        self.assertEqual(len(self.catalogo.listar_postorder()), len(self.catalogo))

    def test_agregar_lugar_con_nombre_duplicado_no_crea_otro_nodo(self):
        """Como `insertar`, la clave repetida actualiza el nodo: la lista crece
        pero el árbol sigue teniendo un nodo por nombre."""
        antes = len(self.catalogo._arbol)
        self.catalogo.agregar_lugar(self.catalogo.buscar("La Biela"))
        self.assertEqual(len(self.catalogo), antes + 1)
        self.assertEqual(len(self.catalogo._arbol), antes)

    def test_agregar_lugar_no_rompe_el_listado_alfabetico(self):
        self.catalogo.agregar_lugar(Lugar(999, "Antes de Todos", "Palermo", "bar", 4.0, "20:00", "02:00", 2))
        self.catalogo.agregar_lugar(Lugar(1000, "Zeta", "Palermo", "bar", 4.0, "20:00", "02:00", 2))
        nombres = [lugar.nombre for lugar in self.catalogo.listar_ordenado()]
        self.assertEqual(len(nombres), len(self.catalogo))
        self.assertEqual(nombres, sorted(nombres, key=str.lower))

    def test_indexar_tolera_cargar_el_mismo_archivo_dos_veces(self):
        """`cargar_desde_json` acumula lugares en la lista, pero el árbol
        indexa una sola vez por clave: recargar no duplica nodos."""
        self.catalogo.cargar_desde_json("datos/lugares.json")
        nombres_unicos = {lugar.nombre for lugar in self.catalogo.listar()}
        self.assertEqual(len(self.catalogo._arbol), len(nombres_unicos))
        self.assertIsNotNone(self.catalogo.buscar_arbol("La Biela"))

    def test_arbol_vacio_no_revienta_la_busqueda(self):
        vacio = Catalogo()
        self.assertIsNone(vacio.buscar_arbol("cualquier cosa"))
        self.assertEqual(vacio.listar_ordenado(), [])
        self.assertEqual(vacio.altura_arbol(), 0)

    def test_altura_arbol_es_logaritmica_en_los_datos_reales(self):
        """50 lugares en orden de carga: la altura debe ser de orden log(n)."""
        altura = self.catalogo.altura_arbol()
        self.assertGreater(altura, 0)
        self.assertLess(altura, 20)

    def test_altura_arbol_escala_con_el_logaritmo_de_n(self):
        """Con n x10, la altura crece ~constantemente (no x10)."""
        alturas = []
        for ruta in ("datos/lugares_100.json",
                     "datos/lugares_1000.json",
                     "datos/lugares_10000.json"):
            catalogo = Catalogo()
            catalogo.cargar_desde_json(ruta)
            alturas.append(catalogo.altura_arbol())
        for anterior, actual in zip(alturas, alturas[1:]):
            self.assertLess(actual - anterior, 20)
        self.assertEqual(alturas, [20, 30, 40])

    def test_indexar_sobre_lista_ya_ordenada_degrada_el_arbol(self):
        """Limitación conocida del BST sin balancear, y la razón del AVL (TP4).

        Fija el comportamiento para que nadie lo reintroduzca por descuido.
        """
        self.catalogo.ordenar_por_titulo()
        self.catalogo.indexar()
        total = len(self.catalogo)
        self.assertEqual(self.catalogo.altura_arbol(), total)

        # Aun degenerado, el árbol sigue siendo correcto: encuentra todo.
        for lugar in self.catalogo.listar():
            with self.subTest(lugar=lugar.nombre):
                self.assertEqual(
                    self.catalogo.buscar_arbol(lugar.nombre).nombre,
                    lugar.nombre,
                )

    def _todos_los_nombres(self):
        return [lugar.nombre for lugar in self.catalogo.listar()]


if __name__ == "__main__":
    unittest.main()
