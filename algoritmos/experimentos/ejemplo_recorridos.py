"""Ejemplos de recorridos del TP5 — árbol general.

Uso:  python algoritmos/experimentos/ejemplo_recorridos.py

Muestra los tres recorridos y las dos formas de buscar sobre (1) el árbol
chico de la consigna y (2) la jerarquía real del catálogo. No mide tiempos: lo
que se compara acá es el ORDEN en que cada recorrido visita los nodos.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from estructuras.arbol_general import ArbolGeneral
from servicios.catalogo import Catalogo, _normalizar


def _flecha(nodos):
    return " → ".join(nodo.etiqueta for nodo in nodos)


def arbol_de_la_consigna() -> ArbolGeneral:
    arbol = ArbolGeneral("Películas", clave=_normalizar)
    ficcion = arbol.agregar(arbol.raiz, "Ciencia ficción")
    arbol.agregar(ficcion, "Cyberpunk")
    arbol.agregar(ficcion, "Viajes temporales")
    arbol.agregar(ficcion, "Inteligencia artificial")
    arbol.agregar(arbol.raiz, "Acción")
    arbol.agregar(arbol.raiz, "Comedia")
    return arbol


def ejemplo_consigna() -> None:
    arbol = arbol_de_la_consigna()
    print("=" * 60)
    print("1) El árbol de la consigna")
    print("=" * 60)
    print("\n".join(arbol.dibujar()))
    print(f"\n{arbol}")

    print("\nRecorridos:")
    print(f"  Preorden    : {_flecha(arbol.preorden())}")
    print(f"  Postorden   : {_flecha(arbol.postorden())}")
    print(f"  Por niveles : {_flecha(arbol.por_niveles())}")

    print("\nPor niveles, agrupado:")
    for numero, nivel in enumerate(arbol.niveles(), start=1):
        print(f"  Nivel {numero}: {', '.join(n.etiqueta for n in nivel)}")

    print("\nBúsquedas:")
    nodo = arbol.buscar("cyberpunk")
    ruta = " > ".join(n.etiqueta for n in arbol.camino(nodo))
    print(f"  buscar('cyberpunk')  -> {ruta}  (nivel {arbol.nivel(nodo)})")
    print(f"  buscar_todos('cia')  -> {_flecha(arbol.buscar_todos('cia'))}")
    print(f"  buscar('Terror')     -> {arbol.buscar('Terror')}")

    # BFS vs DFS: se distinguen cuando una etiqueta se repite a distinta profundidad.
    arbol.agregar(arbol.buscar("Cyberpunk"), "Clásicos")
    arbol.agregar(arbol.raiz, "Clásicos")
    profundo = arbol.buscar_profundidad("Clásicos")
    cercano = arbol.buscar("Clásicos")
    print("\nCon 'Clásicos' repetido (bajo Cyberpunk y directo bajo la raíz):")
    print(f"  buscar (por niveles, BFS)     -> nivel {arbol.nivel(cercano)}")
    print(f"  buscar_profundidad (DFS)      -> nivel {arbol.nivel(profundo)}")


def ejemplo_catalogo() -> None:
    catalogo = Catalogo()
    catalogo.cargar_desde_json(RAIZ / "datos" / "lugares.json")
    catalogo.cargar_categorias_desde_json(RAIZ / "datos" / "categorias.json")
    arbol = catalogo.arbol_categorias

    print("\n" + "=" * 60)
    print("2) La jerarquía real del catálogo")
    print("=" * 60)
    print("\n".join(catalogo.explorar_categorias()))
    print(f"\n{arbol}")

    print("\nRecorridos de grupos y categorías (sin los 50 lugares):")
    for orden in ("preorden", "postorden", "niveles"):
        print(f"  {orden:<10}: {' → '.join(catalogo.recorrer_categorias(orden))}")

    print("\nUna consulta que la lista plana no resuelve:")
    comer = catalogo.lugares_de_rama("Para comer")
    print(f"  lugares_de_rama('Para comer') -> {len(comer)} lugares")
    print(f"  filtrar('Para comer')         -> {len(catalogo.filtrar('Para comer'))} lugares")

    nodo = catalogo.buscar_nodo("Don Julio Parrilla")
    print(f"\nRuta de un lugar: {catalogo.ruta_de(nodo)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ejemplo_consigna()
    ejemplo_catalogo()
