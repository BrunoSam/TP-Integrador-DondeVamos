"""Script de medición del TP2/TP3 — secuencial vs binaria vs árbol BST.

Uso:  python algoritmos/experimentos/medicion.py

Método (idéntico al TP2): `timeit` con 20 ejecuciones x 5 repeticiones y se
conserva el mínimo por llamada; la carga, el ordenamiento y la indexación
se hacen fuera del cronómetro.
"""

import sys
import time
import timeit
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from servicios.catalogo import Catalogo

TAMANOS = (100, 1_000, 10_000, 100_000)

# (etiqueta para la tabla, método del Catalogo)
ESTRATEGIAS = (
    ("secuencial", "buscar"),
    ("binaria", "buscar_binaria"),
    ("arbol", "buscar_arbol"),
)


def medir(func, titulo, number=20, repeat=5) -> float:
    """Devuelve el MEJOR tiempo por llamada en ms (evita ruido de la máquina)."""
    tiempos = timeit.repeat(lambda: func(titulo), number=number, repeat=repeat)
    mejor = min(tiempos) / number
    return mejor * 1000


def sonda(n, nombre_sonda):
    """Consulta de prueba. Ambas existen siempre en el dataset.

    `ultimo` es el peor caso de las tres a la vez; `medio` cae a ~1/3 de la
    altura del árbol.
    """
    if nombre_sonda == "ultimo":
        return f"Lugar {n - 1}"
    if nombre_sonda == "medio":
        return f"Lugar {n // 2}"
    raise ValueError(f"sonda desconocida: {nombre_sonda}")


def obtener_tiempos(nombre_sonda="ultimo") -> dict:
    """Mide las tres estrategias con una sonda.

    Devuelve {"tamanos", "alturas"} y, por estrategia, la lista de tiempos
    en ms para cada tamaño.
    """
    resultados = {"tamanos": [], "alturas": []}
    for etiqueta, _ in ESTRATEGIAS:
        resultados[etiqueta] = []

    for n in TAMANOS:
        catalogo = Catalogo()
        catalogo.cargar_desde_json(f"datos/lugares_{n}.json")
        catalogo.ordenar_por_titulo()  # el costo de ordenar se paga una vez, fuera del cronómetro

        titulo_probe = sonda(n, nombre_sonda)  # existe → no rompe el caso "no encontrado"

        metodos = [(etiqueta, getattr(catalogo, metodo))
                   for etiqueta, metodo in ESTRATEGIAS]

        # warm-up: la primera llamada importa/precalienta y no se cronometra
        for _, metodo in metodos:
            metodo(titulo_probe)

        resultados["tamanos"].append(n)
        resultados["alturas"].append(catalogo.altura_arbol())
        for etiqueta, metodo in metodos:
            resultados[etiqueta].append(medir(metodo, titulo_probe))

    return resultados


def obtener_costos_de_preparacion(repeat=3) -> dict:
    """Cuánto cuesta dejar cada estrategia lista para buscar (una sola vez).

    Cada costo se mide sobre un catálogo FRESCO: si ordenáramos antes de
    indexar, el BST recibiría las claves ya ordenadas y degeneraría.
    """
    costos = {"tamanos": [], "ordenar_ms": [], "indexar_ms": [], "alturas": []}

    for n in TAMANOS:
        ruta = f"datos/lugares_{n}.json"

        catalogo = Catalogo()
        catalogo.cargar_desde_json(ruta)
        ordenar = min(
            _cronometrar(catalogo.ordenar_por_titulo) for _ in range(repeat)
        )

        catalogo = Catalogo()
        catalogo.cargar_desde_json(ruta)
        indexar = min(
            _cronometrar(catalogo.indexar) for _ in range(repeat)
        )

        costos["tamanos"].append(n)
        costos["ordenar_ms"].append(ordenar)
        costos["indexar_ms"].append(indexar)
        costos["alturas"].append(catalogo.altura_arbol())

    return costos


def _cronometrar(func) -> float:
    inicio = time.perf_counter()
    func()
    return (time.perf_counter() - inicio) * 1000


def main() -> None:
    for nombre_sonda in ("ultimo", "medio"):
        datos = obtener_tiempos(nombre_sonda)
        etiqueta_sonda = (
            "ultimo insertado = PEOR caso de las tres"
            if nombre_sonda == "ultimo"
            else "elemento medio = a ~1/3 de la altura del arbol"
        )
        print(f"\n=== Sonda: {sonda(datos['tamanos'][-1], nombre_sonda)}"
              f" ({etiqueta_sonda}) ===")
        print("tamaño\taltura_arbol\tsecuencial_ms\tbinaria_ms\tarbol_ms")
        for i, n in enumerate(datos["tamanos"]):
            print(
                f"{n}\t{datos['alturas'][i]}\t"
                f"{datos['secuencial'][i]:.4f}\t"
                f"{datos['binaria'][i]:.4f}\t"
                f"{datos['arbol'][i]:.4f}"
            )

    costos = obtener_costos_de_preparacion()
    print("\n=== Costo de preparar cada estrategia (una vez, se amortiza) ===")
    print("tamaño\tordenar_ms\tindexar_ms\taltura_arbol")
    for i, n in enumerate(costos["tamanos"]):
        print(
            f"{n}\t{costos['ordenar_ms'][i]:.4f}\t"
            f"{costos['indexar_ms'][i]:.4f}\t"
            f"{costos['alturas'][i]}"
        )


if __name__ == "__main__":
    main()
