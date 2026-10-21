import json
import os
import tempfile
import unittest

from modelos.lugar import Lugar
from servicios.catalogo import Catalogo


def _lugar(id, nombre, categoria, puntuacion=4.0):
    return Lugar(id, nombre, "Palermo", categoria, puntuacion, "10:00", "23:00", 2)


def _catalogo_chico(con_jerarquia=True):
    catalogo = Catalogo()
    for lugar in (
        _lugar(1, "Don Julio", "parrilla", 4.4),
        _lugar(2, "La Cabrera", "parrilla", 4.6),
        _lugar(3, "Chin Chin", "bar", 4.2),
        _lugar(4, "La Biela", "cafeteria", 4.2),
        _lugar(5, "Rapanui", "heladeria", 4.5),
    ):
        catalogo.agregar_lugar(lugar)
    if con_jerarquia:
        _cargar_jerarquia(catalogo)
    return catalogo


def _cargar_jerarquia(catalogo, datos=None):
    datos = datos or {
        "raiz": "Dónde vamos",
        "grupos": {
            "Para comer": ["Parrilla", "Pizzería"],
            "Para tomar algo": ["Bar", "Cafetería"],
        },
    }
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as archivo:
        json.dump(datos, archivo, ensure_ascii=False)
    try:
        catalogo.cargar_categorias_desde_json(archivo.name)
    finally:
        os.remove(archivo.name)


def _etiquetas_de(catalogo, nodo):
    return [n.etiqueta for n in catalogo.arbol_categorias.preorden(nodo)]


class TestArmadoDelArbol(unittest.TestCase):
    def test_catalogo_vacio_tiene_solo_la_raiz(self):
        catalogo = Catalogo()
        self.assertEqual(len(catalogo.arbol_categorias), 1)
        self.assertEqual(catalogo.arbol_categorias.raiz.etiqueta, "Dónde vamos")

    def test_la_jerarquia_cuelga_grupos_y_categorias_de_la_raiz(self):
        catalogo = _catalogo_chico()
        raiz = catalogo.arbol_categorias.raiz
        self.assertEqual(
            [g.etiqueta for g in raiz.hijos],
            ["Para comer", "Para tomar algo", "Otros"],
        )
        comer = raiz.hijos[0]
        self.assertEqual([c.etiqueta for c in comer.hijos], ["Parrilla", "Pizzería"])

    def test_cada_lugar_es_hoja_de_su_categoria(self):
        catalogo = _catalogo_chico()
        parrilla = catalogo.buscar_nodo("parrilla")
        self.assertEqual(
            [h.etiqueta for h in parrilla.hijos], ["Don Julio", "La Cabrera"]
        )
        self.assertTrue(all(h.es_hoja for h in parrilla.hijos))
        self.assertIsInstance(parrilla.hijos[0].valor, Lugar)

    def test_la_categoria_se_engancha_sin_importar_tildes_ni_mayusculas(self):
        catalogo = _catalogo_chico()
        # "Cafetería" (jerarquía) engancha con "cafeteria" (dato del lugar).
        cafeteria = catalogo.buscar_nodo("cafeteria")
        self.assertEqual([h.etiqueta for h in cafeteria.hijos], ["La Biela"])

    def test_categoria_que_no_esta_en_la_jerarquia_va_a_otros(self):
        catalogo = _catalogo_chico()
        self.assertEqual(
            catalogo.ruta_de(catalogo.buscar_nodo("Rapanui")),
            "Dónde vamos > Otros > Heladeria > Rapanui",
        )

    def test_sin_jerarquia_las_categorias_cuelgan_de_la_raiz(self):
        catalogo = _catalogo_chico(con_jerarquia=False)
        raiz = catalogo.arbol_categorias.raiz
        self.assertEqual(
            sorted(c.etiqueta for c in raiz.hijos),
            ["Bar", "Cafeteria", "Heladeria", "Parrilla"],
        )

    def test_ningun_lugar_queda_afuera_del_arbol(self):
        catalogo = _catalogo_chico()
        self.assertEqual(len(catalogo.lugares_de(catalogo.arbol_categorias.raiz)), 5)

    def test_agregar_lugar_lo_cuelga_en_su_categoria(self):
        catalogo = _catalogo_chico()
        catalogo.agregar_lugar(_lugar(6, "Hierro", "parrilla", 4.7))
        parrilla = catalogo.buscar_nodo("Parrilla")
        self.assertEqual(
            [h.etiqueta for h in parrilla.hijos], ["Don Julio", "La Cabrera", "Hierro"]
        )

    def test_agregar_lugar_de_una_categoria_nueva_la_crea(self):
        catalogo = _catalogo_chico()
        catalogo.agregar_lugar(_lugar(6, "Sushi Pop", "sushi"))
        self.assertEqual(
            catalogo.ruta_de(catalogo.buscar_nodo("Sushi Pop")),
            "Dónde vamos > Otros > Sushi > Sushi Pop",
        )

    def test_dos_lugares_con_el_mismo_nombre_quedan_los_dos_en_el_arbol(self):
        catalogo = _catalogo_chico()
        catalogo.agregar_lugar(_lugar(6, "Don Julio", "parrilla"))
        self.assertEqual(len(catalogo.lugares_de_rama("Parrilla")), 3)

    def test_reindexar_conserva_la_jerarquia_cargada(self):
        catalogo = _catalogo_chico()
        catalogo.indexar()
        self.assertEqual(catalogo.buscar_nodo("Para comer").grado, 2)
        self.assertEqual(len(catalogo.lugares_de_rama("Para comer")), 2)

    def test_ordenar_por_titulo_no_cambia_el_arbol(self):
        catalogo = _catalogo_chico()
        antes = catalogo.explorar_categorias(incluir_lugares=True)
        catalogo.ordenar_por_titulo()
        self.assertEqual(catalogo.explorar_categorias(incluir_lugares=True), antes)


class TestConsultas(unittest.TestCase):
    def setUp(self):
        self.catalogo = _catalogo_chico()

    def test_lugares_de_una_categoria(self):
        nombres = [l.nombre for l in self.catalogo.lugares_de_rama("Parrilla")]
        self.assertEqual(nombres, ["Don Julio", "La Cabrera"])

    def test_lugares_de_un_grupo_junta_todas_sus_categorias(self):
        nombres = [l.nombre for l in self.catalogo.lugares_de_rama("para tomar algo")]
        self.assertEqual(nombres, ["Chin Chin", "La Biela"])

    def test_lugares_de_la_raiz_son_todos(self):
        self.assertEqual(len(self.catalogo.lugares_de_rama("Dónde vamos")), 5)

    def test_lugares_de_una_rama_inexistente_es_none(self):
        self.assertIsNone(self.catalogo.lugares_de_rama("Terror"))

    def test_lugares_de_una_categoria_vacia_es_lista_vacia(self):
        # "Pizzería" está en la jerarquía pero no tiene lugares.
        self.assertEqual(self.catalogo.lugares_de_rama("Pizzeria"), [])

    def test_lugares_de_un_lugar_es_el_lugar_mismo(self):
        lugares = self.catalogo.lugares_de_rama("La Biela")
        self.assertEqual([l.nombre for l in lugares], ["La Biela"])

    def test_el_grupo_responde_lo_que_filtrar_no_puede(self):
        por_grupo = {l.nombre for l in self.catalogo.lugares_de_rama("Para tomar algo")}
        por_filtro = {l.nombre for l in self.catalogo.filtrar("bar")} | {
            l.nombre for l in self.catalogo.filtrar("cafeteria")
        }
        self.assertEqual(por_grupo, por_filtro)
        self.assertEqual(self.catalogo.filtrar("para tomar algo"), [])

    def test_buscar_nodo_encuentra_grupos_categorias_y_lugares(self):
        self.assertIsNotNone(self.catalogo.buscar_nodo("Para comer"))
        self.assertIsNotNone(self.catalogo.buscar_nodo("BAR"))
        self.assertIsNotNone(self.catalogo.buscar_nodo("la biela"))
        self.assertIsNone(self.catalogo.buscar_nodo("Terror"))

    def test_buscar_nodos_parcial_devuelve_todas_las_coincidencias(self):
        etiquetas = [n.etiqueta for n in self.catalogo.buscar_nodos("la ")]
        self.assertEqual(etiquetas, ["La Cabrera", "La Biela"])

    def test_ruta_de_un_lugar(self):
        nodo = self.catalogo.buscar_nodo("Chin Chin")
        self.assertEqual(
            self.catalogo.ruta_de(nodo),
            "Dónde vamos > Para tomar algo > Bar > Chin Chin",
        )

    def test_describir_nodo(self):
        self.assertEqual(
            self.catalogo.describir_nodo(self.catalogo.buscar_nodo("Parrilla")),
            "Parrilla (2 lugares)",
        )
        self.assertEqual(
            self.catalogo.describir_nodo(self.catalogo.buscar_nodo("Bar")),
            "Bar (1 lugar)",
        )
        self.assertEqual(
            self.catalogo.describir_nodo(self.catalogo.buscar_nodo("Don Julio")),
            "Don Julio (⭐ 4.4)",
        )


class TestPresentacion(unittest.TestCase):
    def setUp(self):
        self.catalogo = _catalogo_chico()

    def test_explorar_muestra_grupos_y_categorias_sin_lugares(self):
        self.assertEqual(self.catalogo.explorar_categorias(), [
            "Dónde vamos (5 lugares)",
            "├── Para comer (2 lugares)",
            "│   ├── Parrilla (2 lugares)",
            "│   └── Pizzería (0 lugares)",
            "├── Para tomar algo (2 lugares)",
            "│   ├── Bar (1 lugar)",
            "│   └── Cafetería (1 lugar)",
            "└── Otros (1 lugar)",
            "    └── Heladeria (1 lugar)",
        ])

    def test_explorar_con_lugares_los_incluye(self):
        lineas = self.catalogo.explorar_categorias(incluir_lugares=True)
        self.assertEqual(len(lineas), len(self.catalogo.arbol_categorias))
        self.assertIn("│   │   ├── Don Julio (⭐ 4.4)", lineas)

    def test_recorridos_de_categorias_excluyen_los_lugares(self):
        self.assertEqual(self.catalogo.recorrer_categorias("preorden"), [
            "Dónde vamos", "Para comer", "Parrilla", "Pizzería",
            "Para tomar algo", "Bar", "Cafetería", "Otros", "Heladeria",
        ])
        self.assertEqual(self.catalogo.recorrer_categorias("postorden"), [
            "Parrilla", "Pizzería", "Para comer", "Bar", "Cafetería",
            "Para tomar algo", "Heladeria", "Otros", "Dónde vamos",
        ])
        self.assertEqual(self.catalogo.recorrer_categorias("niveles"), [
            "Dónde vamos", "Para comer", "Para tomar algo", "Otros",
            "Parrilla", "Pizzería", "Bar", "Cafetería", "Heladeria",
        ])

    def test_recorrer_desde_un_grupo(self):
        grupo = self.catalogo.buscar_nodo("Para comer")
        self.assertEqual(
            self.catalogo.recorrer_categorias("preorden", grupo),
            ["Para comer", "Parrilla", "Pizzería"],
        )

    def test_recorrido_desconocido_falla(self):
        with self.assertRaises(ValueError):
            self.catalogo.recorrer_categorias("inorder")


class TestDatosReales(unittest.TestCase):
    """Con el dataset de 50 lugares y la jerarquía que se entrega en datos/."""

    @classmethod
    def setUpClass(cls):
        cls.catalogo = Catalogo()
        cls.catalogo.cargar_desde_json("datos/lugares.json")
        cls.catalogo.cargar_categorias_desde_json("datos/categorias.json")

    def test_los_50_lugares_estan_en_el_arbol(self):
        raiz = self.catalogo.arbol_categorias.raiz
        self.assertEqual(len(self.catalogo.lugares_de(raiz)), 50)
        self.assertEqual(len(self.catalogo), 50)

    def test_la_jerarquia_cubre_todas_las_categorias_reales(self):
        self.assertIsNone(self.catalogo.buscar_nodo("Otros"))

    def test_las_hojas_son_los_lugares_del_catalogo_sin_repetir(self):
        del_arbol = {l.id for l in self.catalogo.lugares_de(
            self.catalogo.arbol_categorias.raiz)}
        self.assertEqual(del_arbol, {l.id for l in self.catalogo.listar()})

    def test_los_grupos_suman_el_total(self):
        raiz = self.catalogo.arbol_categorias.raiz
        suma = sum(len(self.catalogo.lugares_de(g)) for g in raiz.hijos)
        self.assertEqual(suma, 50)

    def test_cada_categoria_coincide_con_filtrar(self):
        for categoria in ("parrilla", "bar", "cafeteria", "heladeria",
                          "restaurante", "pizzeria", "bodegon"):
            del_arbol = {l.id for l in self.catalogo.lugares_de_rama(categoria)}
            del_filtro = {l.id for l in self.catalogo.filtrar(categoria)}
            self.assertEqual(del_arbol, del_filtro, categoria)

    def test_el_arbol_tiene_cuatro_niveles(self):
        # raíz > grupo > categoría > lugar
        self.assertEqual(self.catalogo.arbol_categorias.altura(), 4)
        self.assertEqual(len(self.catalogo.arbol_categorias), 1 + 3 + 7 + 50)


if __name__ == "__main__":
    unittest.main()
