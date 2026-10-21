# ¿Dónde vamos?

Proyecto integrador de **Estructura de Datos**, desarrollado en Python.

## Descripción

¿Dónde vamos? es un sistema que ayuda a parejas o grupos pequeños de amigos a
encontrar y organizar una salida considerando sus preferencias y presupuesto.

Su **v3** (TP1 a TP5) permite:

- **Buscar un lugar** por coincidencia parcial (recorrido lineal sobre la lista).
- **Buscar por nombre exacto** comparando **cuatro estrategias** de búsqueda: secuencial O(n), binaria O(log n) sobre lista ordenada, árbol binario de búsqueda O(log n) y **árbol AVL O(log n) garantizado**. La opción 5 de la terminal deja elegir y cronometra cada una.
- **Comparar BST vs AVL** con el mismo catálogo insertado en orden alfabético (opción 6): muestra cómo el BST degenera y el AVL no.
- **Listar** todos los lugares en orden de carga o **en orden alfabético** (recorrido *inorder* del árbol).
- **Filtrar** por categoría y **ver** los participantes de cada salida.
- **Explorar categorías** (opción 7): una jerarquía `Dónde vamos > Para comer > Parrilla > lugares` implementada con un **árbol general**. Se puede navegar nivel por nivel, buscar un nodo y ver su ruta, pedir **todos los lugares de un grupo** (algo que `filtrar` no puede) y ver los recorridos preorden, postorden y por niveles.

Los árboles del TP3, TP4 y TP5 se integraron como **estructuras complementarias**, no
como reemplazo de la lista: `filtrar` y la búsqueda parcial siguen siendo lineales a
propósito, porque un árbol no puede responderlas en O(log n).

## Estado del proyecto

| TP | Tema | Estado |
|---|---|---|
| TP0 | Propuesta y lanzamiento | ✅ |
| TP1 | Objetos y clases — modelo, catálogo y terminal v1 | ✅ |
| TP2 | Análisis de algoritmos — secuencial vs binaria | ✅ |
| TP3 | Árbol binario de búsqueda | ✅ |
| TP4 | AVL | ✅ |
| TP5 | Árbol general | ✅ |
| TP6 | Heap (Top 10 de lugares) | ⏳ |
| TP7 | Grafo (lugares relacionados) | ⏳ |
| TP8 | BFS / DFS | ⏳ |
| TP9 | Caminos mínimos (Dijkstra) | ⏳ |
| TP10 | Producto final | ⏳ |

## Ejecución

```bash
python main.py
```

No requiere instalar nada: solo Python 3.10 o superior y la biblioteca estándar.

## Pruebas

```bash
python -m unittest discover tests
```

199 pruebas (`tests/test_catalogo.py`, `tests/test_arbol_binario.py`,
`tests/test_arbol_avl.py`, `tests/test_arbol_general.py`,
`tests/test_catalogo_categorias.py` y `tests/test_terminal_categorias.py`), sin
dependencias externas.

> Una prueba de escala (`test_altura_arbol_escala_con_el_logaritmo_de_n`) usa los
> datasets sintéticos, que están en `.gitignore`: en un clon limpio hay que correr
> primero `python datos/generar.py`.

## Experimentos

```bash
python datos/generar.py                          # datasets sintéticos (100 a 100.000)
python algoritmos/experimentos/medicion.py       # mide las tres estrategias del TP2/TP3
python algoritmos/experimentos/grafico.py        # guarda docs/capturas/experimento-tp3.png
python algoritmos/experimentos/medicion_avl.py   # BST vs AVL por orden de inserción (TP4)
python algoritmos/experimentos/grafico_avl.py    # guarda docs/capturas/experimento-tp4.png
python algoritmos/experimentos/ejemplo_recorridos.py  # recorridos del árbol general (TP5)
```

- Informe TP2 (secuencial vs binaria): [`docs/tp2-experimentos.md`](docs/tp2-experimentos.md)
- Informe TP3 (agrega el BST): [`docs/tp3-arbol-binario.md`](docs/tp3-arbol-binario.md)
- Informe TP4 (BST vs AVL y desbalance): [`docs/tp4-avl.md`](docs/tp4-avl.md)
- Informe TP5 (árbol general y jerarquía de categorías): [`docs/tp5-arbol-general.md`](docs/tp5-arbol-general.md)

## Documentación

| Doc | Contenido |
|---|---|
| [`docs/01-requerimientos.md`](docs/01-requerimientos.md) | Alcance, RF/RNF con estado estable, criterios de aceptación y observaciones |
| [`docs/02-casos-de-uso.md`](docs/02-casos-de-uso.md) | Diagrama general y 6 casos de uso textuales |
| [`docs/03-diagrama-clases.md`](docs/03-diagrama-clases.md) | Clases del dominio, `Catalogo`, `ArbolBinarioBusqueda`, `ArbolAVL` y `ArbolGeneral` |
| [`docs/04-diagrama-datos.md`](docs/04-diagrama-datos.md) | Flujo de datos: de los JSON crudos a la terminal, pasando por cada estructura |
| [`docs/05-gestion-proyecto.md`](docs/05-gestion-proyecto.md) | Tablero, sprints, historias de usuario y retros |

## Demo

| | |
|---|---|
| ![Buscar lugar](docs/capturas/tp1-demo-buscar.png) | ![Filtrar por categoría](docs/capturas/tp1-demo-filtrar.png) |
| Buscar lugar (v1) | Filtrar por categoría (v1) |

![Listar lugares](docs/capturas/tp1-demo-Listar.png)

## Estructura del repositorio

```text
TP0_Donde_Vamos/
├── main.py
├── README.md
├── .gitignore
├── docs/
│   ├── 01-requerimientos.md
│   ├── 02-casos-de-uso.md
│   ├── 03-diagrama-clases.md
│   ├── 04-diagrama-datos.md
│   ├── 05-gestion-proyecto.md
│   ├── tp2-experimentos.md
│   ├── tp3-arbol-binario.md
│   ├── tp4-avl.md
│   ├── tp5-arbol-general.md
│   └── capturas/
├── modelos/
│   ├── lugar.py
│   └── salida.py
├── servicios/
│   └── catalogo.py          ← búsqueda secuencial, binaria, BST y AVL + jerarquía de categorías
├── estructuras/
│   ├── arbol_binario.py     ← TP3: NodoArbol y ArbolBinarioBusqueda
│   ├── arbol_avl.py         ← TP4: NodoAVL y ArbolAVL
│   └── arbol_general.py     ← TP5: NodoGeneral y ArbolGeneral (n-ario)
├── ui/
│   └── terminal.py          ← v3 (5: estrategias · 6: BST vs AVL · 7: explorar categorías)
├── datos/
│   ├── lugares.json
│   ├── categorias.json      ← TP5: jerarquía grupos > categorías
│   ├── salidas.json
│   └── generar.py           ← TP2: datasets sintéticos (los generados están en .gitignore)
├── algoritmos/
│   └── experimentos/
│       ├── medicion.py      ← TP2 + TP3
│       ├── grafico.py
│       ├── medicion_avl.py  ← TP4
│       ├── grafico_avl.py
│       └── ejemplo_recorridos.py  ← TP5
└── tests/
    ├── test_catalogo.py
    ├── test_arbol_binario.py
    ├── test_arbol_avl.py
    ├── test_arbol_general.py            ← TP5
    ├── test_catalogo_categorias.py      ← TP5
    └── test_terminal_categorias.py      ← TP5
```

## Evolución

En **TP0** se documentó la propuesta y se preparó el repositorio. En **TP1** se
implementó la v1: modelo de dominio, catálogo con búsqueda exacta y parcial sin
distinguir mayúsculas, terminal desacoplada de la lógica y un dataset de 50 lugares
reales de CABA. En **TP2** se analizó la complejidad de la búsqueda por nombre,
comparando la estrategia secuencial (O(n)) con una binaria sobre lista ordenada
(O(log n)) y verificando el RNF01 con datasets de 100 a 100.000 lugares. En **TP3**
se implementó el árbol binario de búsqueda, se integró al catálogo como tercera
estrategia de búsqueda exacta y como fuente del listado alfabético, y se comparó
contra las dos anteriores **sin cambiar la metodología** del TP2.

El resultado del TP3 fue incómodo y quedó documentado tal cual: el BST **no le ganó
a `bisect`** en velocidad de búsqueda (`bisect` es código C), pero resuelve la
inserción en O(log n) sin reordenar toda la lista. Además degenera a O(n) si las
claves llegan ordenadas, que es exactamente lo que nos pasó al medir el costo de
preparación. Ver [`docs/tp3-arbol-binario.md`](docs/tp3-arbol-binario.md) §8 y §9.

En **TP4** se resolvió esa deuda con un **AVL**: la misma estructura de búsqueda,
pero con rotaciones que mantienen la altura en O(log n) **garantizado**, sin
importar cómo lleguen las claves. Se agregó como cuarta estrategia del catálogo y
como opción 6 de la terminal, y se midió contra el BST variando el orden de
inserción: con 10.000 datos ordenados el BST queda con altura 10.000 y el AVL con
altura 14 (buscar pasa de 1,52 ms a 0,0019 ms). El trade-off quedó documentado sin
disimular: con datos aleatorios el AVL construye ~2,4× más lento. Ver
[`docs/tp4-avl.md`](docs/tp4-avl.md).

En **TP5** se sumó una estructura de otra naturaleza: un **árbol general (n-ario)**
que no sirve para buscar más rápido sino para **organizar por significado**. El
catálogo ahora tiene una jerarquía `Dónde vamos > grupo > categoría > lugar`
(61 nodos, altura 4, cargada desde `datos/categorias.json`) que responde lo que la
lista plana no puede: `lugares_de_rama('Para comer')` devuelve 20 lugares, mientras
`filtrar('Para comer')` devuelve 0. Se integró como la opción 7 de la terminal
(versión 3) con navegación por niveles, búsqueda con ruta y los tres recorridos.
El informe deja explícito lo que el árbol **no** aporta: no acelera ninguna
búsqueda y un nodo solo puede tener un padre, límite que motiva el grafo del TP7.
Ver [`docs/tp5-arbol-general.md`](docs/tp5-arbol-general.md).
