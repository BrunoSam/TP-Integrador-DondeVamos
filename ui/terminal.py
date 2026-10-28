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
            elif opcion == "7":
                self._explorar_categorias()
            elif opcion == "8":
                self._ver_top_n()
            elif opcion == "0":
                print("¡Hasta la próxima!")
                break
            else:
                print("Opción inválida.")

            print()

    def _mostrar_menu(self) -> None:
        print("=" * 45)
        print("   🌳 ¿DÓNDE VAMOS? — TERMINAL (v4)")
        print("=" * 45)
        print("1. Buscar lugar (coincidencia parcial)")
        print("2. Listar todos los lugares")
        print("3. Filtrar por categoría")
        print("4. Ver participantes por salida")
        print("5. Buscar por nombre exacto (comparar estrategias)")
        print("6. Comparar BST vs AVL (desbalance)")
        print("7. Explorar categorías (árbol general)")
        print("8. Ver Top N recomendaciones")
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
        """Compara las tres estrategias de búsqueda exacta sobre una consulta."""
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

    def _explorar_categorias(self) -> None:
        """Submenú del TP5: la jerarquía grupos > categorías > lugares."""
        while True:
            print("\n--- EXPLORAR CATEGORÍAS ---")
            print("1. Navegar la jerarquía (entrar y subir de nivel)")
            print("2. Ver el árbol de categorías")
            print("3. Ver el árbol completo (con los lugares)")
            print("4. Buscar en el árbol y ver su ruta")
            print("5. Ver los lugares de una rama (ej: todo \"Para comer\")")
            print("6. Recorridos: preorden, postorden y por niveles")
            print("0. Volver al menú principal")

            opcion = input("Opción: ").strip()

            if opcion == "1":
                self._navegar_categorias()
            elif opcion == "2":
                print()
                print("\n".join(self._catalogo.explorar_categorias()))
            elif opcion == "3":
                print()
                print("\n".join(self._catalogo.explorar_categorias(incluir_lugares=True)))
            elif opcion == "4":
                self._buscar_en_arbol()
            elif opcion == "5":
                self._lugares_de_rama()
            elif opcion == "6":
                self._mostrar_recorridos()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")

    def _navegar_categorias(self) -> None:
        """Navegación interactiva: se baja eligiendo un número y se sube con 0."""
        actual = self._catalogo.arbol_categorias.raiz

        while True:
            print(f"\nEstás en: {self._catalogo.ruta_de(actual)}")
            hijos = actual.hijos

            if not hijos:
                print("  (no hay nada más abajo)")
            for numero, hijo in enumerate(hijos, start=1):
                print(f"  {numero}. {self._catalogo.describir_nodo(hijo)}")

            destino = "Volver" if actual.padre is None else "Subir un nivel"
            print(f"  0. {destino}")

            opcion = input("Elegí: ").strip()

            if opcion == "0":
                if actual.padre is None:
                    return
                actual = actual.padre
            elif opcion.isdigit() and 1 <= int(opcion) <= len(hijos):
                elegido = hijos[int(opcion) - 1]
                if elegido.valor is not None:
                    print()
                    print(elegido.valor)
                else:
                    actual = elegido
            else:
                print("Opción inválida.")

    def _buscar_en_arbol(self) -> None:
        texto = input("Texto a buscar (grupo, categoría o lugar): ").strip()

        if not texto:
            print("No escribiste nada.")
            return

        nodos = self._catalogo.buscar_nodos(texto)

        if not nodos:
            print(f"No encontramos '{texto}' en el árbol.")
            return

        print(f"\n--- {len(nodos)} COINCIDENCIAS ---")
        for nodo in nodos:
            print(f"  {self._catalogo.ruta_de(nodo)}")

    def _lugares_de_rama(self) -> None:
        nombre = input("Grupo o categoría: ").strip()

        lugares = self._catalogo.lugares_de_rama(nombre)

        if lugares is None:
            print(f"No existe '{nombre}' en el árbol.")
        elif not lugares:
            print(f"'{nombre}' no tiene lugares cargados.")
        else:
            print(f"\n--- {nombre.upper()}: {len(lugares)} LUGARES ---")
            for lugar in lugares:
                print()
                print(lugar)

    def _mostrar_recorridos(self) -> None:
        """Los tres recorridos sobre grupos y categorías, con qué aporta cada uno."""
        nombre = input("Recorrer desde (Enter = toda la jerarquía): ").strip()

        desde = None
        if nombre:
            desde = self._catalogo.buscar_nodo(nombre)
            if desde is None:
                print(f"No existe '{nombre}' en el árbol.")
                return

        recorridos = (
            ("preorden", "Preorden", "el padre antes que sus hijos (se lee como un índice)"),
            ("postorden", "Postorden", "los hijos antes que su padre (lo específico primero)"),
            ("niveles", "Por niveles", "de lo general a lo específico, nivel por nivel"),
        )
        for clave, titulo, explicacion in recorridos:
            etiquetas = self._catalogo.recorrer_categorias(clave, desde)
            print(f"\n--- {titulo}: {explicacion} ---")
            print("  " + " → ".join(etiquetas))

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

    def _ver_top_n(self) -> None:
        try:
            n_str = input("¿Cuántos elementos mostrar en el Top-N? ").strip()
            n = int(n_str)
        except Exception:
            print("Ingresá un número válido.")
            return
        if n <= 0:
            print("El número debe ser mayor a 0.")
            return
        top = self._catalogo.obtener_top_n(n)
        print(f"\n--- TOP {n} ---")
        for i, lugar in enumerate(top, 1):
            print(f"{i}. {lugar}")
