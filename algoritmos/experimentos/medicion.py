"""Script de medición del TP2 — búsqueda secuencial vs binaria.

Uso:  python algoritmos/experimentos/medicion.py
Mide el tiempo de búsqueda por nombre con datos/lugares_{n}.json.
Mismo dataset y misma consulta ("Lugar {n-1}", existe) en ambas estrategias.
"""

import sys
import timeit
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from servicios.catalogo import Catalogo


def medir(func, titulo, number=20, repeat=5) -> float:
    """Devuelve el MEJOR tiempo por llamada en ms (evita ruido de la máquina)."""
    tiempos = timeit.repeat(lambda: func(titulo), number=number, repeat=repeat)
    mejor = min(tiempos) / number
    return mejor * 1000


def obtener_tiempos():
    """Devuelve (tamaños, tiempos_secuencial_ms, tiempos_binaria_ms)."""
    tamaños = []
    secuencial = []
    binaria = []
    for n in (100, 1_000, 10_000, 100_000):
        catalogo = Catalogo()
        catalogo.cargar_desde_json(f"datos/lugares_{n}.json")
        catalogo.ordenar_por_titulo()  # el costo de ordenar se paga una vez, fuera del cronómetro

        titulo_probe = f"Lugar {n - 1}"  # existe → no rompe el caso "no encontrado"

        # warm-up: la primera llamada importa/precalienta y no se cronometra
        catalogo.buscar(titulo_probe)
        catalogo.buscar_binaria(titulo_probe)

        t_sec = medir(catalogo.buscar, titulo_probe)
        t_bin = medir(catalogo.buscar_binaria, titulo_probe)
        tamaños.append(n)
        secuencial.append(t_sec)
        binaria.append(t_bin)
    return tamaños, secuencial, binaria


def main() -> None:
    print("tamaño\tsecuencial_ms\tbinaria_ms")
    for n, t_sec, t_bin in zip(*obtener_tiempos()):
        print(f"{n}\t{t_sec:.4f}\t\t{t_bin:.4f}")


if __name__ == "__main__":
    main()