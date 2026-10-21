import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from servicios.catalogo import Catalogo
from ui.terminal import Terminal


def _terminal():
    catalogo = Catalogo()
    catalogo.cargar_desde_json("datos/lugares.json")
    catalogo.cargar_categorias_desde_json("datos/categorias.json")
    return Terminal(catalogo)


def _correr(metodo, entradas):
    """Ejecuta un método de la terminal con `input` simulado y devuelve lo impreso."""
    salida = io.StringIO()
    with patch("builtins.input", side_effect=entradas), redirect_stdout(salida):
        metodo()
    return salida.getvalue()


class TestTerminalCategorias(unittest.TestCase):
    def test_navegar_baja_hasta_un_lugar_y_vuelve_a_subir(self):
        # Para comer > Parrilla > (lugar 1) > subir, subir, subir > volver
        texto = _correr(
            _terminal()._navegar_categorias,
            ["1", "1", "1", "0", "0", "0"],
        )
        self.assertIn("Estás en: Dónde vamos > Para comer > Parrilla", texto)
        self.assertIn("Parrilla Sanabria Palermo", texto)
        self.assertIn("⭐", texto)
        self.assertIn("0. Volver", texto)

    def test_navegar_rechaza_opciones_invalidas_sin_romperse(self):
        texto = _correr(_terminal()._navegar_categorias, ["99", "abc", "0"])
        self.assertEqual(texto.count("Opción inválida."), 2)

    def test_lugares_de_una_rama_por_grupo(self):
        texto = _correr(_terminal()._lugares_de_rama, ["Para comer"])
        self.assertIn("20 LUGARES", texto)

    def test_lugares_de_una_rama_inexistente(self):
        texto = _correr(_terminal()._lugares_de_rama, ["Terror"])
        self.assertIn("No existe 'Terror'", texto)

    def test_buscar_en_arbol_muestra_la_ruta(self):
        texto = _correr(_terminal()._buscar_en_arbol, ["cafeteria"])
        self.assertIn("Dónde vamos > Para tomar algo > Cafetería", texto)

    def test_recorridos_desde_la_raiz(self):
        texto = _correr(_terminal()._mostrar_recorridos, [""])
        self.assertIn("Preorden", texto)
        self.assertIn("Postorden", texto)
        self.assertIn("Por niveles", texto)
        self.assertTrue(texto.rstrip().splitlines()[-1].strip().startswith("Dónde vamos"))

    def test_recorridos_desde_un_grupo(self):
        texto = _correr(_terminal()._mostrar_recorridos, ["Algo dulce"])
        self.assertIn("Algo dulce → Heladería", texto)

    def test_el_submenu_se_puede_cerrar(self):
        texto = _correr(_terminal()._explorar_categorias, ["2", "0"])
        self.assertIn("Para comer (20 lugares)", texto)


if __name__ == "__main__":
    unittest.main()
