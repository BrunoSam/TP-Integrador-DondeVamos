import time

from servicios.catalogo import Catalogo

ESTRATEGIAS = {
    "1": ("Secuencial", "buscar", "O(n): recorre la lista"),
    "2": ("Binaria", "buscar_binaria", "O(log n): lista ordenada"),
    "3": ("Árbol BST", "buscar_arbol", "O(log n) promedio: índice BST"),
    "4": ("Árbol AVL", "buscar_avl", "O(log n) garantizado: índice AVL"),
}


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
            elif opcion == "5":
                self._buscar_exacto()
            elif opcion == "6":
                self._comparar_arboles()
            elif opcion == "0":
                print("¡Hasta la próxima!")
                break
            else:
                print("Opción inválida.")

            print()

    def _mostrar_menu(self) -> None:
        print("=" * 45)
        print("   🌳 ¿DÓNDE VAMOS? — TERMINAL (v2)")
        print("=" * 45)
        print("1. Buscar lugar (coincidencia parcial)")
        print("2. Listar todos los lugares")
        print("3. Filtrar por categoría")
        print("4. Ver participantes por salida")
        print("5. Buscar por nombre exacto (comparar estrategias)")
        print("6. Comparar BST vs AVL (desbalance)")
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

    def _buscar_exacto(self) -> None:
        """Compara las cuatro estrategias de búsqueda exacta sobre una consulta."""
        nombre = input("Nombre exacto: ").strip()

        if not nombre:
            print("No escribiste nada.")
            return

        print("\nEstrategias:")
        for opcion, (titulo, _, complejidad) in ESTRATEGIAS.items():
            print(f"  {opcion}) {titulo:<12} {complejidad}")
        print("  5) Las cuatro")

        opcion = input("Estrategia: ").strip()

        if opcion == "5":
            elegidas = list(ESTRATEGIAS)
        elif opcion in ESTRATEGIAS:
            elegidas = [opcion]
        else:
            print("Opción inválida.")
            return

        # El costo de ordenar se paga una vez, acá y fuera del cronómetro.
        self._catalogo.ordenar_por_titulo()

        for clave in elegidas:
            titulo, metodo, complejidad = ESTRATEGIAS[clave]
            buscar = getattr(self._catalogo, metodo)

            inicio = time.perf_counter()
            lugar = buscar(nombre)
            elapsed_ms = (time.perf_counter() - inicio) * 1000

            print(f"\n--- {titulo} ({complejidad}) ---")
            if lugar is None:
                print(f"  No se encontró '{nombre}'.")
            else:
                print(f"  {lugar}")
            print(f"  Tiempo: {elapsed_ms:.5f} ms")

        print(
            f"\nCatálogo: {len(self._catalogo)} lugares"
            f" · altura del BST: {self._catalogo.altura_arbol()} niveles"
            f" · altura del AVL: {self._catalogo.altura_avl()} niveles"
        )

    def _comparar_arboles(self) -> None:
        """Mini ejemplo del TP4: el mismo catálogo insertado EN ORDEN
        ALFABÉTICO degenera el BST y deja al AVL balanceado."""
        medidas = self._catalogo.comparar_bst_vs_avl()
        n = len(self._catalogo)

        print(f"\n--- BST vs AVL con {n} lugares en orden alfabético ---")
        print(f"{'Árbol':<6}{'Altura':>8}{'Construcción':>16}")
        for etiqueta in ("BST", "AVL"):
            datos = medidas[etiqueta]
            print(f"{etiqueta:<6}{datos['altura']:>8}{datos['ms']:>13.4f} ms")

        print("\nEl BST degenera en una lista enlazada (altura = n): buscar pasa")
        print("de O(log n) a O(n). El AVL se rebalancea con rotaciones y mantiene")
        print("la altura en O(log n) sin importar el orden de inserción.")

    def _listar(self) -> None:
        print("\nOrden:")
        print("  1) Orden de carga (como viene del archivo)")
        print("  2) Orden alfabético (recorrido inorder del árbol)")

        opcion = input("Opción: ").strip()

        if opcion == "2":
            lugares = self._catalogo.listar_ordenado()
        else:
            lugares = self._catalogo.listar()

        if not lugares:
            print("No hay lugares para listar.")
            return

        print(f"\n--- LUGARES ({len(lugares)}) ---")

        for lugar in lugares:
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
