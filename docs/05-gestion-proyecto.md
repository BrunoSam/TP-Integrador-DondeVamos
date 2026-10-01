# Gestión del proyecto

- **Tablero:** https://trello.com/b/s3XjcekO/tp-integrador-estructuras-de-datos-donde-vamos
- **Metodología:** Scrum simplificado — un sprint por TP, columnas: `Backlog · En progreso · En revisión · Hecho`.
- **Integrantes:** Alan Ledesma, Natalia Elias y Bruno Sammarco.

---

## Sprint TP0 (Lanzamiento)

Historias:

- [x] Como equipo quiero elegir el universo del proyecto para definir el alcance.
  - Criterio: dominio justificado y con datos disponibles.
- [x] Como equipo queremos un problema y un usuario objetivo concretos.
  - Criterio: el enunciado dice a quién le sirve y qué le duele hoy.
- [x] Como equipo queremos una propuesta inicial de 1 página para comunicar la idea.
  - Criterio: 5 funcionalidades + usuario objetivo.
- [x] Como equipo queremos el repo listo para empezar.
  - Criterio: README, `.gitignore` y estructura de carpetas.
- [x] Como equipo queremos un boceto del diagrama de clases.
  - Criterio: `Lugar`, `Catalogo`, `Salida` y `Terminal` esbozados en `docs/03`.
- [ ] Como equipo queremos el tablero con las 5 funcionalidades cargadas como tarjetas.
  - Criterio: las 5 tarjetas están en la columna Backlog.
- [ ] Como equipo queremos enviar la nómina del grupo al docente.

**Retro TP0**:

Se definió un problema concreto, un usuario objetivo y un alcance inicial acotado. El modelo y los requerimientos pudieron refinarse en las etapas siguientes a partir de la implementación y de las estructuras de datos de la cursada.

## Sprint TP1 (Objetos y clases — v1)

Historias:

- [x] Como usuario quiero buscar un lugar por su nombre exacto para encontrarlo rápido.
  - Criterio: no distingue mayúsculas ni tildes; devuelve el `Lugar` o `None`.
- [x] Como usuario quiero buscar por coincidencia parcial para no tener que recordar el nombre completo.
  - Criterio: "palermo" encuentra todos los lugares de esa zona.
- [x] Como usuario quiero ver la lista completa para explorar el catálogo.
- [x] Como usuario quiero filtrar por categoría para no recorrer todo a mano.
  - Criterio: filtro case-insensitive sobre `categoria`.
- [x] Como usuario quiero ver quién participa de cada salida para saber quién va.
- [x] Como equipo queremos que la lógica esté separada de la interfaz para poder probarla sin UI.
  - Criterio: `Catalogo` no hace `input()` ni `print()` de menú; las pruebas corren sin la terminal.
- [x] Como equipo queremos un dataset real para probar con información creíble.
  - Criterio: 50 lugares de CABA con puntuación, costo y horarios.
- [x] Como equipo queremos pruebas unitarias que corran sin dependencias externas.
  - Criterio: `python -m unittest discover tests` pasa.

**Retro TP1**:

Se implementó la v1 completa: `Lugar` con encapsulamiento (`@property`, `__repr__`), catálogo con búsqueda exacta y parcial sin distinguir mayúsculas, y terminal desacoplada de la lógica. El dataset quedó con 50 lugares reales de CABA.

Qué mejorar: sumar más datos reales a medida que crece el catálogo y arrancar el hábito de commits por unidad de trabajo (la historia del repo se evalúa).

## Sprint TP2 (Complejidad)

Historias:

- [x] Como equipo queremos identificar la operación crítica del sistema.
  - Criterio: la búsqueda exacta por nombre, que es la que el usuario más ejecuta.
- [x] Como equipo queremos comparar esa operación con una segunda estrategia.
  - Criterio: secuencial O(n) contra binaria O(log n) sobre lista ordenada.
- [x] Como equipo queremos medir con distintos volúmenes, no con 50 datos.
  - Criterio: datasets de 100, 1.000, 10.000 y 100.000 lugares, generados por un script commiteado.
- [x] Como equipo queremos que la medición no mienta.
  - Criterio: `timeit` con mínimo por llamada, warm-up, carga y ordenamiento fuera del cronómetro, misma consulta en ambas estrategias.
- [x] Como equipo queremos expresar el resultado en notación de complejidad.
  - Criterio: tabla O/Ω/Θ para cada estrategia.
- [x] Como equipo queremos documentar el experimento.
  - Criterio: `docs/tp2-experimentos.md` con método, tabla, gráfico y conclusión.

**Retro TP2**:

Se identificó la operación crítica y se comparó con dos estrategias. El hallazgo que más sirvió: con 100 elementos las dos "andan igual" (menos de 1 ms), y la diferencia asintótica recién aparece cuando el volumen crece. Eso justifica el RNF01.

Qué mejorar: el script medía una sola consulta, y esa consulta resultó ser el peor caso para las dos estrategias a la vez. Para TP3 se agregó una segunda sonda.

## Sprint TP3 (Árbol binario de búsqueda)

Historias:

- [x] Como equipo queremos un BST genérico, no atado al dominio.
  - Criterio: la clave se inyecta como `callable`; el árbol no importa nada de `servicios/`.
- [x] Como equipo queremos las tres operaciones del enunciado.
  - Criterio: inserción, búsqueda y recorridos inorder/preorder/postorder, todos iterativos.
- [x] Como usuario quiero que el árbol resuelva una función real, no ser un juguete.
  - Criterio: la opción 5 de la terminal busca por nombre exacto con las tres estrategias y cronometra cada una.
- [x] Como usuario quiero el mismo nombre con tildes, minúsculas y acentos.
  - Criterio: las tres estrategias usan la misma `_normalizar`.
- [x] Como equipo queremos comparar el árbol contra el TP2 sin cambiar la metodología.
  - Criterio: mismos tamaños, mismo `timeit` 20×5 con mínimo, misma sonda `ultimo`.
  - Criterio: se agrega una segunda sonda, porque `ultimo` es peor caso para las tres y eso desfavorece al árbol.
- [x] Como equipo queremos que el balance del árbol sea verificable.
  - Criterio: la altura se expone y hay una prueba que falla si el árbol se degenera.
- [x] Como equipo queremos que los docs reflejen la estructura nueva.
  - Criterio: 03 con las clases del árbol, 04 con el flujo de datos completo.
- [x] Como equipo queremos integrar el árbol que subió cada integrante sin duplicar estructuras.
  - Criterio: una sola implementación de BST en `estructuras/`; el `Catalogo` expone los tres recorridos y el alta incremental.

**Retro TP3**:

El árbol entró como índice complementario, no como reemplazo de la lista: `filtrar` y `buscar_parcial` siguen siendo lineales porque el BST no puede responderlas en O(log n). La medición dejó una lección que no esperábamos: en Python el BST resulta más lento que `bisect`, porque `bisect` es código C. El valor del árbol no es la velocidad en la búsqueda, sino que insertar un lugar nuevo cuesta O(log n) en lugar de un `sort` de O(n log n).

El merge de las dos versiones del árbol encontró un bug que las pruebas no veían: `postorder()` se saltaba el subárbol izquierdo de cualquier nodo sin hijo derecho, y con los 50 lugares reales devolvía 48. Se detectó recién al agregar las pruebas de los recorridos a través del catálogo, y se corrigió comparando los recorridos contra el conjunto de valores en vez de contra una lista escrita a mano.

Qué mejorar: el árbol se desbalancea si las inserciones llegan ya ordenadas (altura = n). El AVL del TP4 es la respuesta.

---

## Pendientes de gestión

- [ ] Cargar las historias de TP3 como tarjetas en el tablero de Trello.
- [ ] Enviar la nómina del grupo al docente.
