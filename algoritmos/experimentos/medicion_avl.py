"""Experimento del TP4 — BST sin balancear vs AVL con datos que degeneran.

Uso:  python algoritmos/experimentos/medicion_avl.py

Compara la MISMA operación (búsqueda exacta por nombre normalizado) en dos
versiones de la estructura —el BST del TP3 y el AVL del TP4— sobre el MISMO
dataset, variando el ORDEN en que llegan las claves:

    aleatorio      el caso típico, donde el BST se porta bien
    ascendente     peor caso del BST: degenera a lista enlazada (altura = n)
    descendente    el espejo del anterior (también degenera)
    casi_ordenado  ordenado con ~1% de vecinos intercambiados (caso realista)

Metodología (idéntica al TP2/TP3): carga fuera del cronómetro, warm-up por
estructura, y `timeit` (20 ejecuciones × 5 repeticiones) quedándonos con el
mínimo por llamada. La construcción se cronometra una sola vez.

Por qué los tamaños degenerados se recortan a 10.000: construir un BST con las
claves ya ordenadas es O(n²). A 100.000 serían ~5·10⁹ comparaciones en Python
interpretado, o sea minutos por corrida. El AVL, en cambio, construye en
O(n log n), así que el recorte no lo favorece: es solo para que el script corra.
"""

import random
import sys
import time
import timeit
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_binario import ArbolBinarioBusqueda
from servicios.catalogo import Catalogo, _normalizar

TAMANOS_ALEATORIO = (100, 1_000, 10_000, 100_000)
TAMANOS_DEGENERADO = (100, 1_000, 10_000)
TIPOS = ("aleatorio", "ascendente", "descendente", "casi_ordenado")

ESTRUCTURAS = (("bst", ArbolBinarioBusqueda), ("avl", ArbolAVL))


def _cargar_lugares(n):
    """Carga un dataset con el mismo camino que la aplicación (fuera del cronómetro)."""
    catalogo = Catalogo()
    catalogo.cargar_desde_json(f"datos/lugares_{n}.json")
    return catalogo.listar()


def _dataset(lugares, tipo):
    """Reordena el mismo conjunto de lugares según el tipo de caso."""
    if tipo == "aleatorio":
        datos = list(lugares)
        random.shuffle(datos)
        return datos

    ordenados = sorted(lugares, key=lambda lugar: _normalizar(lugar.nombre))
    if tipo == "ascendente":
        return ordenados
    if tipo == "descendente":
        return list(reversed(ordenados))
    if tipo == "casi_ordenado":
        datos = list(ordenados)
        for i in range(0, len(datos) - 1, 100):  # ~1% de vecinos intercambiados
            datos[i], datos[i + 1] = datos[i + 1], datos[i]
        return datos
    raise ValueError(f"tipo desconocido: {tipo}")


def _construir(clase, lugares):
    """Construye el árbol y devuelve `(arbol, ms)` con la construcción cronometrada."""
    arbol = clase(clave=lambda lugar: _normalizar(lugar.nombre))
    inicio = time.perf_counter()
    for lugar in lugares:
        arbol.insertar(lugar)
    return arbol, (time.perf_counter() - inicio) * 1000


def _clave_mas_profunda(arbol):
    """Devuelve `(clave, profundidad)` del nodo más profundo: el peor caso de búsqueda."""
    pila = [(arbol.raiz, 1)]
    mejor_clave, mejor_profundidad = None, 0
    while pila:
        nodo, profundidad = pila.pop()
        if profundidad > mejor_profundidad:
            mejor_clave, mejor_profundidad = nodo.clave, profundidad
        if nodo.izquierdo is not None:
            pila.append((nodo.izquierdo, profundidad + 1))
        if nodo.derecho is not None:
            pila.append((nodo.derecho, profundidad + 1))
    return mejor_clave, mejor_profundidad


def medir_busqueda(arbol, clave, number=20, repeat=5) -> float:
    """Mejor tiempo por búsqueda en ms, igual que en el TP2/TP3."""
    tiempos = timeit.repeat(lambda: arbol.buscar(clave), number=number, repeat=repeat)
    return min(tiempos) / number * 1000


def obtener_resultados() -> dict:
    """Mide BST y AVL para cada combinación (tipo, tamaño)."""
    random.seed(42)  # reproducible: el orden "aleatorio" es siempre el mismo
    resultados = {}

    for tipo in TIPOS:
        tamanos = TAMANOS_ALEATORIO if tipo == "aleatorio" else TAMANOS_DEGENERADO
        registro = {
            "tamanos": list(tamanos),
            "bst": {"altura": [], "profundidad": [], "construccion_ms": [], "busqueda_ms": []},
            "avl": {"altura": [], "profundidad": [], "construccion_ms": [], "busqueda_ms": []},
        }

        for n in tamanos:
            datos = _dataset(_cargar_lugares(n), tipo)

            for etiqueta, clase in ESTRUCTURAS:
                arbol, ms_construccion = _construir(clase, datos)
                peor_clave, profundidad = _clave_mas_profunda(arbol)
                arbol.buscar(peor_clave)  # warm-up

                registro[etiqueta]["altura"].append(arbol.altura())
                registro[etiqueta]["profundidad"].append(profundidad)
                registro[etiqueta]["construccion_ms"].append(ms_construccion)
                registro[etiqueta]["busqueda_ms"].append(medir_busqueda(arbol, peor_clave))

        resultados[tipo] = registro

    return resultados


def _imprimir_tabla(tipo, registro) -> None:
    print(f"\n=== Orden de inserción: {tipo} ===")
    print(
        f"{'N':>8}\t{'estructura':>11}\t{'altura':>7}\t{'peor prof.':>10}\t"
        f"{'construir_ms':>13}\t{'buscar_ms':>10}"
    )
    for i, n in enumerate(registro["tamanos"]):
        for etiqueta in ("bst", "avl"):
            fila = registro[etiqueta]
            print(
                f"{n:>8}\t{etiqueta.upper():>11}\t{fila['altura'][i]:>7}\t"
                f"{fila['profundidad'][i]:>10}\t{fila['construccion_ms'][i]:>13.4f}\t"
                f"{fila['busqueda_ms'][i]:>10.4f}"
            )


def main() -> None:
    resultados = obtener_resultados()
    for tipo in TIPOS:
        _imprimir_tabla(tipo, resultados[tipo])


if __name__ == "__main__":
    main()
