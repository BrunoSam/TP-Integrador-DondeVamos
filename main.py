import sys

from servicios.catalogo import Catalogo
from ui.terminal import Terminal


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    catalogo = Catalogo()
    catalogo.cargar_desde_json("datos/lugares.json")
    catalogo.cargar_salidas_desde_json("datos/salidas.json")
    print(f"Se cargaron {len(catalogo)} lugares.")
    Terminal(catalogo).iniciar()


if __name__ == "__main__":
    main()