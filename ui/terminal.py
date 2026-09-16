from servicios.catalogo import Catalogo


class Terminal:
    """Interfaz de línea de comandos."""

    def __init__(self, catalogo: Catalogo) -> None:
        self._catalogo = catalogo

    def iniciar(self) -> None:
        while True:
            self._mostrar_menu()

            opcion = input("Opción: ").strip()

            if opcion == "1":
                self._buscar()
            elif opcion == "2":
                self._listar()
            elif opcion == "3":
                self._filtrar()
            elif opcion == "4":
                self._participantes()
            elif opcion == "0":
                print("¡Hasta la próxima!")
                break
            else:
                print("Opción inválida.")

            print()

    def _mostrar_menu(self) -> None:
        print("=" * 45)
        print("   🌳 ¿DÓNDE VAMOS? — TERMINAL (v1)")
        print("=" * 45)
        print("1. Buscar lugar")
        print("2. Listar todos los lugares")
        print("3. Filtrar por categoría")
        print("4. Ver participantes por salida")
        print("0. Salir")
        print("-" * 45)

    def _buscar(self) -> None:
        nombre = input(
            "Nombre a buscar: "
        ).strip()

        resultados = self._catalogo.buscar_parcial(nombre)

        if resultados:
            print("\n--- RESULTADOS ---")

            for lugar in resultados:
                print()
                print(lugar)
        else:
            print(
                f"No encontramos '{nombre}'."
            )

    def _listar(self) -> None:
        print("\n--- LUGARES ---")

        for lugar in self._catalogo.listar():
            print()
            print(lugar)

    def _filtrar(self) -> None:
        categoria = input(
            "Categoría: "
        ).strip()

        resultados = self._catalogo.filtrar(categoria)

        if resultados:
            print("\n--- RESULTADOS ---")

            for lugar in resultados:
                print()
                print(lugar)
        else:
            print(
                f"No hay lugares en '{categoria}'."
            )

    def _participantes(self) -> None:
        print("\n--- PARTICIPANTES ---")

        for salida in self._catalogo.listar_salidas():
            print(f"\nSalida: {salida.nombre}")

            for participante in salida.participantes:
                print(f"- {participante}")