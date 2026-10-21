import unittest

from estructuras.arbol_general import ArbolGeneral, NodoGeneral
from servicios.catalogo import _normalizar


def _peliculas():
    """El árbol de la consigna del TP5. Devuelve (arbol, nodos por etiqueta)."""
    arbol = ArbolGeneral("Películas", clave=_normalizar)
    n = {"Películas": arbol.raiz}
    n["Ciencia ficción"] = arbol.agregar(arbol.raiz, "Ciencia ficción")
    n["Cyberpunk"] = arbol.agregar(n["Ciencia ficción"], "Cyberpunk")
    n["Viajes temporales"] = arbol.agregar(n["Ciencia ficción"], "Viajes temporales")
    n["Inteligencia artificial"] = arbol.agregar(
        n["Ciencia ficción"], "Inteligencia artificial"
    )
    n["Acción"] = arbol.agregar(arbol.raiz, "Acción")
    n["Comedia"] = arbol.agregar(arbol.raiz, "Comedia")
    return arbol, n


def _etiquetas(nodos):
    return [nodo.etiqueta for nodo in nodos]


class TestConstruccion(unittest.TestCase):
    def test_arbol_nuevo_solo_tiene_la_raiz(self):
        arbol = ArbolGeneral("Raíz")
        self.assertEqual(arbol.raiz.etiqueta, "Raíz")
        self.assertEqual(len(arbol), 1)
        self.assertEqual(arbol.altura(), 1)
        self.assertTrue(arbol.raiz.es_hoja)
        self.assertIsNone(arbol.raiz.padre)

    def test_agregar_devuelve_el_nodo_y_lo_cuelga_del_padre(self):
        arbol = ArbolGeneral("Raíz")
        hijo = arbol.agregar(arbol.raiz, "Hijo", valor=42)
        self.assertIsInstance(hijo, NodoGeneral)
        self.assertIs(hijo.padre, arbol.raiz)
        self.assertEqual(hijo.valor, 42)
        self.assertEqual(arbol.raiz.hijos, (hijo,))
        self.assertEqual(len(arbol), 2)

    def test_un_nodo_puede_tener_muchos_hijos(self):
        arbol = ArbolGeneral("Raíz")
        for i in range(100):
            arbol.agregar(arbol.raiz, f"h{i}")
        self.assertEqual(arbol.raiz.grado, 100)
        self.assertEqual(len(arbol), 101)

    def test_los_hijos_conservan_el_orden_de_alta(self):
        arbol, n = _peliculas()
        self.assertEqual(
            _etiquetas(n["Películas"].hijos), ["Ciencia ficción", "Acción", "Comedia"]
        )

    def test_hijos_es_una_tupla_y_no_deja_modificar_el_arbol(self):
        arbol, n = _peliculas()
        with self.assertRaises(AttributeError):
            n["Películas"].hijos.append(NodoGeneral("intruso"))
        self.assertEqual(n["Películas"].grado, 3)

    def test_no_se_puede_colgar_de_un_nodo_ajeno(self):
        arbol, _ = _peliculas()
        otro = ArbolGeneral("Otro")
        with self.assertRaises(ValueError):
            arbol.agregar(otro.raiz, "x")
        self.assertEqual(len(arbol), 7)

    def test_se_permiten_hermanos_con_la_misma_etiqueta(self):
        arbol = ArbolGeneral("Raíz")
        arbol.agregar(arbol.raiz, "Starbucks")
        arbol.agregar(arbol.raiz, "Starbucks")
        self.assertEqual(arbol.raiz.grado, 2)


class TestRecorridos(unittest.TestCase):
    def setUp(self):
        self.arbol, self.n = _peliculas()

    def test_preorden_es_el_orden_de_lectura(self):
        self.assertEqual(
            _etiquetas(self.arbol.preorden()),
            ["Películas", "Ciencia ficción", "Cyberpunk", "Viajes temporales",
             "Inteligencia artificial", "Acción", "Comedia"],
        )

    def test_postorden_deja_los_hijos_antes_que_el_padre(self):
        self.assertEqual(
            _etiquetas(self.arbol.postorden()),
            ["Cyberpunk", "Viajes temporales", "Inteligencia artificial",
             "Ciencia ficción", "Acción", "Comedia", "Películas"],
        )

    def test_por_niveles_va_de_lo_general_a_lo_especifico(self):
        self.assertEqual(
            _etiquetas(self.arbol.por_niveles()),
            ["Películas", "Ciencia ficción", "Acción", "Comedia", "Cyberpunk",
             "Viajes temporales", "Inteligencia artificial"],
        )

    def test_niveles_agrupa_por_nivel(self):
        niveles = [_etiquetas(nivel) for nivel in self.arbol.niveles()]
        self.assertEqual(niveles, [
            ["Películas"],
            ["Ciencia ficción", "Acción", "Comedia"],
            ["Cyberpunk", "Viajes temporales", "Inteligencia artificial"],
        ])

    def test_los_tres_recorridos_visitan_los_mismos_nodos(self):
        todos = {id(nodo) for nodo in self.arbol.preorden()}
        self.assertEqual(len(todos), len(self.arbol))
        self.assertEqual({id(x) for x in self.arbol.postorden()}, todos)
        self.assertEqual({id(x) for x in self.arbol.por_niveles()}, todos)

    def test_la_raiz_es_primera_en_preorden_y_ultima_en_postorden(self):
        self.assertIs(self.arbol.preorden()[0], self.arbol.raiz)
        self.assertIs(self.arbol.postorden()[-1], self.arbol.raiz)

    def test_recorrer_un_subarbol(self):
        rama = self.n["Ciencia ficción"]
        self.assertEqual(
            _etiquetas(self.arbol.preorden(rama)),
            ["Ciencia ficción", "Cyberpunk", "Viajes temporales", "Inteligencia artificial"],
        )
        self.assertEqual(
            _etiquetas(self.arbol.postorden(rama))[-1], "Ciencia ficción"
        )

    def test_hojas(self):
        self.assertEqual(
            _etiquetas(self.arbol.hojas()),
            ["Cyberpunk", "Viajes temporales", "Inteligencia artificial",
             "Acción", "Comedia"],
        )
        self.assertEqual(_etiquetas(self.arbol.hojas(self.n["Comedia"])), ["Comedia"])

    def test_recorrer_desde_un_nodo_ajeno_falla(self):
        with self.assertRaises(ValueError):
            self.arbol.preorden(ArbolGeneral("Otro").raiz)


class TestBusquedas(unittest.TestCase):
    def setUp(self):
        self.arbol, self.n = _peliculas()

    def test_buscar_devuelve_el_nodo(self):
        self.assertIs(self.arbol.buscar("Cyberpunk"), self.n["Cyberpunk"])

    def test_buscar_no_distingue_mayusculas_ni_tildes_con_la_clave_inyectada(self):
        self.assertIs(self.arbol.buscar("ACCION"), self.n["Acción"])
        self.assertIs(self.arbol.buscar("ciencia ficcion"), self.n["Ciencia ficción"])

    def test_buscar_sin_clave_inyectada_es_exacto(self):
        arbol = ArbolGeneral("Raíz")
        arbol.agregar(arbol.raiz, "Acción")
        self.assertIsNone(arbol.buscar("accion"))
        self.assertIsNotNone(arbol.buscar("Acción"))

    def test_buscar_inexistente_devuelve_none(self):
        self.assertIsNone(self.arbol.buscar("Terror"))

    def test_buscar_encuentra_la_raiz(self):
        self.assertIs(self.arbol.buscar("peliculas"), self.arbol.raiz)

    def test_buscar_desde_un_subarbol_no_ve_el_resto(self):
        self.assertIsNone(self.arbol.buscar("Comedia", desde=self.n["Ciencia ficción"]))
        self.assertIs(
            self.arbol.buscar("Cyberpunk", desde=self.n["Ciencia ficción"]),
            self.n["Cyberpunk"],
        )

    def test_buscar_todos_por_coincidencia_parcial(self):
        self.assertEqual(
            _etiquetas(self.arbol.buscar_todos("cia")),
            ["Ciencia ficción", "Inteligencia artificial"],
        )
        # Una coincidencia más corta atrapa más nodos: "ia" está en cuatro.
        self.assertEqual(len(self.arbol.buscar_todos("ia")), 4)

    def test_buscar_todos_sin_coincidencias_devuelve_lista_vacia(self):
        self.assertEqual(self.arbol.buscar_todos("zzz"), [])

    def test_contiene_y_operador_in(self):
        self.assertTrue(self.arbol.contiene("Comedia"))
        self.assertIn("comedia", self.arbol)
        self.assertNotIn("Terror", self.arbol)

    def test_bfs_devuelve_el_match_mas_cercano_y_dfs_el_primero_en_lectura(self):
        # "Clásicos" aparece profundo en la primera rama y superficial en la segunda.
        arbol = ArbolGeneral("Raíz", clave=_normalizar)
        a = arbol.agregar(arbol.raiz, "A")
        a1 = arbol.agregar(a, "A1")
        profundo = arbol.agregar(a1, "Clásicos")
        superficial = arbol.agregar(arbol.raiz, "Clásicos")

        self.assertIs(arbol.buscar("clasicos"), superficial)
        self.assertIs(arbol.buscar_profundidad("clasicos"), profundo)


class TestPosicion(unittest.TestCase):
    def setUp(self):
        self.arbol, self.n = _peliculas()

    def test_nivel_cuenta_desde_1(self):
        self.assertEqual(self.arbol.nivel(self.arbol.raiz), 1)
        self.assertEqual(self.arbol.nivel(self.n["Acción"]), 2)
        self.assertEqual(self.arbol.nivel(self.n["Cyberpunk"]), 3)

    def test_camino_va_de_la_raiz_al_nodo(self):
        self.assertEqual(
            _etiquetas(self.arbol.camino(self.n["Viajes temporales"])),
            ["Películas", "Ciencia ficción", "Viajes temporales"],
        )
        self.assertEqual(_etiquetas(self.arbol.camino(self.arbol.raiz)), ["Películas"])

    def test_camino_de_un_nodo_ajeno_falla(self):
        with self.assertRaises(ValueError):
            self.arbol.camino(ArbolGeneral("Otro").raiz)

    def test_altura_es_el_mayor_nivel(self):
        self.assertEqual(self.arbol.altura(), 3)

    def test_grado_y_es_hoja(self):
        self.assertEqual(self.n["Ciencia ficción"].grado, 3)
        self.assertFalse(self.n["Ciencia ficción"].es_hoja)
        self.assertTrue(self.n["Comedia"].es_hoja)


class TestEliminar(unittest.TestCase):
    def setUp(self):
        self.arbol, self.n = _peliculas()

    def test_eliminar_borra_todo_el_subarbol(self):
        removidos = self.arbol.eliminar(self.n["Ciencia ficción"])
        self.assertEqual(removidos, 4)
        self.assertEqual(len(self.arbol), 3)
        self.assertEqual(
            _etiquetas(self.arbol.preorden()), ["Películas", "Acción", "Comedia"]
        )
        self.assertIsNone(self.arbol.buscar("Cyberpunk"))

    def test_eliminar_una_hoja(self):
        self.assertEqual(self.arbol.eliminar(self.n["Comedia"]), 1)
        self.assertEqual(len(self.arbol), 6)

    def test_el_tamano_coincide_con_los_nodos_recorridos(self):
        self.arbol.eliminar(self.n["Viajes temporales"])
        self.assertEqual(len(self.arbol), len(self.arbol.preorden()))

    def test_no_se_puede_eliminar_la_raiz(self):
        with self.assertRaises(ValueError):
            self.arbol.eliminar(self.arbol.raiz)
        self.assertEqual(len(self.arbol), 7)

    def test_un_nodo_eliminado_ya_no_pertenece_al_arbol(self):
        self.arbol.eliminar(self.n["Acción"])
        with self.assertRaises(ValueError):
            self.arbol.eliminar(self.n["Acción"])
        with self.assertRaises(ValueError):
            self.arbol.agregar(self.n["Acción"], "Bélicas")


class TestDibujar(unittest.TestCase):
    def test_dibuja_el_arbol_de_la_consigna(self):
        arbol, _ = _peliculas()
        self.assertEqual(arbol.dibujar(), [
            "Películas",
            "├── Ciencia ficción",
            "│   ├── Cyberpunk",
            "│   ├── Viajes temporales",
            "│   └── Inteligencia artificial",
            "├── Acción",
            "└── Comedia",
        ])

    def test_ultima_rama_no_arrastra_la_barra_vertical(self):
        arbol = ArbolGeneral("R")
        a = arbol.agregar(arbol.raiz, "A")
        arbol.agregar(a, "A1")
        self.assertEqual(arbol.dibujar(), ["R", "└── A", "    └── A1"])

    def test_max_nivel_limita_la_profundidad(self):
        arbol, _ = _peliculas()
        self.assertEqual(arbol.dibujar(max_nivel=2), [
            "Películas", "├── Ciencia ficción", "├── Acción", "└── Comedia",
        ])
        self.assertEqual(arbol.dibujar(max_nivel=1), ["Películas"])

    def test_dibujar_desde_un_subarbol(self):
        arbol, n = _peliculas()
        self.assertEqual(arbol.dibujar(desde=n["Ciencia ficción"]), [
            "Ciencia ficción",
            "├── Cyberpunk",
            "├── Viajes temporales",
            "└── Inteligencia artificial",
        ])

    def test_formato_personalizado(self):
        arbol, _ = _peliculas()
        lineas = arbol.dibujar(max_nivel=2, formato=lambda n: n.etiqueta.upper())
        self.assertEqual(lineas[0], "PELÍCULAS")
        self.assertEqual(lineas[-1], "└── COMEDIA")


class TestJerarquiasProfundas(unittest.TestCase):
    """Todo es iterativo: una cadena larga no puede reventar la recursión."""

    PROFUNDIDAD = 3000  # el límite de recursión de Python es ~1000

    def _cadena(self):
        arbol = ArbolGeneral("n0")
        actual = arbol.raiz
        for i in range(1, self.PROFUNDIDAD):
            actual = arbol.agregar(actual, f"n{i}")
        return arbol, actual

    def test_recorridos_y_medidas_sobre_una_cadena_profunda(self):
        arbol, ultimo = self._cadena()
        self.assertEqual(arbol.altura(), self.PROFUNDIDAD)
        self.assertEqual(len(arbol.preorden()), self.PROFUNDIDAD)
        self.assertEqual(len(arbol.postorden()), self.PROFUNDIDAD)
        self.assertEqual(len(arbol.por_niveles()), self.PROFUNDIDAD)
        self.assertEqual(arbol.nivel(ultimo), self.PROFUNDIDAD)
        self.assertIs(arbol.buscar(f"n{self.PROFUNDIDAD - 1}"), ultimo)

    def test_dibujar_una_cadena_profunda(self):
        arbol, _ = self._cadena()
        self.assertEqual(len(arbol.dibujar(max_nivel=1500)), 1500)

    def test_eliminar_una_rama_profunda(self):
        arbol, _ = self._cadena()
        self.assertEqual(arbol.eliminar(arbol.raiz.hijos[0]), self.PROFUNDIDAD - 1)
        self.assertEqual(len(arbol), 1)


class TestRepr(unittest.TestCase):
    def test_repr_resume_el_arbol(self):
        arbol, _ = _peliculas()
        self.assertEqual(
            repr(arbol), "ArbolGeneral(raiz='Películas', tamano=7, altura=3)"
        )


if __name__ == "__main__":
    unittest.main()
