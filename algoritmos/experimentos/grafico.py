"""Genera el gráfico log-log del experimento (opcional).

Uso:  python algoritmos/experimentos/grafico.py
Usa los tiempos reales de la medición y guarda la imagen en
docs/capturas/experimento-tp3.png
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib no está instalado; el gráfico es opcional.")
    sys.exit(0)

from algoritmos.experimentos.medicion import ESTRATEGIAS, obtener_tiempos


def main() -> None:
    datos = obtener_tiempos("ultimo")
    tamanos = datos["tamanos"]

    print(f"{'N':>8}\t{'altura':>8}" + "".join(
        f"{etiqueta + '_ms':>16}" for etiqueta, _ in ESTRATEGIAS
    ))
    for i, n in enumerate(tamanos):
        fila = f"{n:>8}\t{datos['alturas'][i]:>8}"
        for etiqueta, _ in ESTRATEGIAS:
            fila += f"{datos[etiqueta][i]:>16.4f}"
        print(fila)

    for etiqueta, _ in ESTRATEGIAS:
        plt.plot(tamanos, datos[etiqueta], label=etiqueta, marker="o")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("N elementos")
    plt.ylabel("Tiempo (ms)")
    plt.title("Búsqueda exacta por nombre: secuencial vs binaria vs árbol BST (log-log)")
    plt.legend()
    plt.grid(True, which="both", ls=":")

    salida = Path(__file__).resolve().parents[2] / "docs" / "capturas" / "experimento-tp3.png"
    salida.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(salida)
    print(f"\nGráfico guardado en {salida}")


if __name__ == "__main__":
    main()
