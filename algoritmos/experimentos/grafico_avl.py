"""Genera el gráfico de altura del experimento TP4 (BST vs AVL).

Uso:  python algoritmos/experimentos/grafico_avl.py
Usa las alturas reales de la medición y guarda la imagen en
docs/capturas/experimento-tp4.png

La lectura del gráfico es la tesis del TP4: la altura del BST con datos
ordenados es una recta de pendiente 1 (lineal, O(n)); la del AVL es casi plana
(logarítmica, O(log n)), sin importar el orden en que lleguen las claves.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib no está instalado; el gráfico es opcional.")
    sys.exit(0)

from algoritmos.experimentos.medicion_avl import obtener_resultados


def main() -> None:
    resultados = obtener_resultados()

    series = (
        ("BST · aleatorio", "aleatorio", "bst", "tab:orange", "o"),
        ("BST · ordenado", "ascendente", "bst", "tab:red", "s"),
        ("AVL · aleatorio", "aleatorio", "avl", "tab:blue", "^"),
        ("AVL · ordenado", "ascendente", "avl", "tab:green", "D"),
    )

    for etiqueta, tipo, estructura, color, marcador in series:
        registro = resultados[tipo]
        plt.plot(
            registro["tamanos"],
            registro[estructura]["altura"],
            label=etiqueta,
            color=color,
            marker=marcador,
        )

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("N elementos")
    plt.ylabel("Altura del árbol (niveles)")
    plt.title("TP4 — Altura: BST sin balancear vs AVL (log-log)")
    plt.legend()
    plt.grid(True, which="both", ls=":")

    salida = Path(__file__).resolve().parents[2] / "docs" / "capturas" / "experimento-tp4.png"
    salida.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(salida)
    print(f"Gráfico guardado en {salida}")

    # La tabla de alturas, para que el número quede junto al gráfico.
    print(f"\n{'N':>8}\t{'BST aleat.':>11}\t{'BST orden.':>11}\t{'AVL aleat.':>11}\t{'AVL orden.':>11}")
    tamanos = resultados["ascendente"]["tamanos"]
    for i, n in enumerate(tamanos):
        print(
            f"{n:>8}\t{resultados['aleatorio']['bst']['altura'][i]:>11}\t"
            f"{resultados['ascendente']['bst']['altura'][i]:>11}\t"
            f"{resultados['aleatorio']['avl']['altura'][i]:>11}\t"
            f"{resultados['ascendente']['avl']['altura'][i]:>11}"
        )


if __name__ == "__main__":
    main()
