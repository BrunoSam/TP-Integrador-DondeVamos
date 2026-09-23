"""Genera el gráfico log-log del experimento TP2 (opcional).

Uso:  python algoritmos/experimentos/grafico.py
Usa los tiempos reales de la medición y guarda la imagen en docs/capturas/experimento-tp2.png
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib no está instalado; el gráfico es opcional.")
    sys.exit(0)

from algoritmos.experimentos.medicion import obtener_tiempos


def main() -> None:
    tamaños, secuencial, binaria = obtener_tiempos()
    print(f"{'N':>8}\t{'secuencial_ms':>14}\t{'binaria_ms':>11}")
    for n, s, b in zip(tamaños, secuencial, binaria):
        print(f"{n:>8}\t{s:>14.4f}\t{b:>11.4f}")

    plt.plot(tamaños, secuencial, label="secuencial", marker="o")
    plt.plot(tamaños, binaria, label="binaria", marker="s")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("N elementos")
    plt.ylabel("Tiempo (ms)")
    plt.title("Búsqueda por nombre: secuencial vs binaria (log-log)")
    plt.legend()
    plt.grid(True, which="both", ls=":")

    salida = Path(__file__).resolve().parents[2] / "docs" / "capturas" / "experimento-tp2.png"
    salida.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(salida)
    print(f"Gráfico guardado en {salida}")


if __name__ == "__main__":
    main()