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

Qué mejorar:

- El árbol se desbalancea si las inserciones llegan ya ordenadas (altura = n). El AVL del TP4 es la respuesta.
- El TP3 entró en **un solo commit** (`efaad7d`), así que no respetamos el compromiso del retro del TP1 de commits por unidad de trabajo. La causa fue práctica: el trabajo del TP3 y el merge del árbol del equipo quedaron intercalados en los mismos archivos, y con el plazo de las 00:00 separar el historial exigía stagear porciones de archivo a mano. Además, rehacer el commit después habría movido su fecha al día siguiente y hecho que el TP3 pareciera entregado fuera de plazo. Queda asumido: el hábito se retoma en el TP4.

---

## Sprint TP4 (Árbol AVL)

Historias:

- [x] Como equipo queremos entender y reproducir el desbalance del BST del TP3.
  - Criterio: casos de inserción ordenada ascendente, descendente y casi ordenada, con la altura medida y comparada contra n.
- [x] Como equipo queremos un AVL genérico, no atado al dominio.
  - Criterio: `estructuras/arbol_avl.py` con inserción que rebalancea con las cuatro rotaciones, clave inyectada como `callable` y misma API que el BST.
- [x] Como equipo queremos garantizar O(log n) y poder verificarlo.
  - Criterio: ningún nodo con `|factor de balance| > 1` y altura acotada por `1,44·log₂(n+2)`; hay pruebas que lo fijan.
- [x] Como usuario quiero poder usar el AVL desde la aplicación.
  - Criterio: `buscar_avl` como cuarta estrategia en la opción 5 y demo BST vs AVL en la opción 6.
- [x] Como equipo queremos comparar BST contra AVL en los casos de desbalance.
  - Criterio: misma metodología de medición del TP2/TP3, variando el **orden** de inserción; tabla de altura, construcción y búsqueda.
- [x] Como equipo queremos documentar el experimento.
  - Criterio: `docs/tp4-avl.md` con método, tablas, gráfico y conclusión técnica.
- [x] Como equipo queremos retomar los commits por unidad de trabajo.
  - Criterio: el TP4 entra en commits separados (estructura AVL, integración, experimento, documentación).

**Retro TP4**:

El AVL resolvió la deuda del TP3: con rotaciones de costo O(1) mantiene `|factor de balance| ≤ 1` y, con eso, la altura en O(log n) garantizado. Un efecto lateral que no esperábamos documentar: el AVL **hace segura la recursión**, porque la altura queda acotada a ~24 niveles para 100.000 claves; por eso la inserción puede ser recursiva, a diferencia del BST del TP3 que tuvo que ser iterativo.

El experimento confirmó la degeneración y agregó un dato: **"casi ordenado" es casi tan malo como "ordenado"** —con 1% de vecinos intercambiados el BST quedó con altura 9.900 sobre 10.000, o sea el 99% de n—. No hace falta que los datos lleguen perfectamente ordenados para romper el BST.

También quedó claro el **costo** del AVL: con datos aleatorios construye ~2,4× más lento que el BST. Su ventaja no es ser rápido en el caso típico, es serlo en el peor caso. El trade-off es overhead constante por garantía asintótica, y lo dejamos escrito sin disimularlo, igual que el resultado incómodo del TP3.

Qué mejorar:

- El AVL no implementa eliminación (el BST tampoco); agregarla obliga a más casos de rotación al borrar. Queda como extensión natural.
- Repetir la medición en otra máquina para separar lo reproducible (alturas, patrón de crecimiento) del ruido (tiempos en el rango de microsegundos, donde las tablas se cruzan).

---

## Pendientes de gestión

- [ ] Cargar las historias de TP3 y TP4 como tarjetas en el tablero de Trello.
- [ ] Enviar la nómina del grupo al docente.
- [x] Abrir el TP4 con commits por unidad de trabajo, como en el TP2: estructura AVL, integración en el catálogo y medición.
