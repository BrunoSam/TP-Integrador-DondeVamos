# ¿Dónde vamos?

Proyecto integrador de **Estructura de Datos**, desarrollado en Python.

## Descripción

¿Dónde vamos? es un sistema que ayuda a parejas o grupos pequeños de amigos a
encontrar y organizar una salida considerando sus preferencias y presupuesto.

Su **v2** (TP1 + TP2 + TP3 + TP4) permite:

- **Buscar un lugar** por coincidencia parcial (recorrido lineal sobre la lista).
- **Buscar por nombre exacto** comparando **cuatro estrategias** de búsqueda: secuencial O(n), binaria O(log n) sobre lista ordenada, árbol binario de búsqueda O(log n) y **árbol AVL O(log n) garantizado**. La opción 5 de la terminal deja elegir y cronometra cada una.
- **Comparar BST vs AVL** con el mismo catálogo insertado en orden alfabético (opción 6): muestra cómo el BST degenera y el AVL no.
- **Listar** todos los lugares en orden de carga o **en orden alfabético** (recorrido *inorder* del árbol).
- **Filtrar** por categoría y **ver** los participantes de cada salida.

Los árboles del TP3 y del TP4 se integraron como **índices complementarios**, no
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
| TP5 | Árbol general | ⏳ |
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

112 pruebas (`tests/test_catalogo.py`, `tests/test_arbol_binario.py` y
`tests/test_arbol_avl.py`), sin dependencias externas.

## Experimentos

```bash
python datos/generar.py                          # datasets sintéticos (100 a 100.000)
python algoritmos/experimentos/medicion.py       # mide las tres estrategias del TP2/TP3
python algoritmos/experimentos/grafico.py        # guarda docs/capturas/experimento-tp3.png
python algoritmos/experimentos/medicion_avl.py   # BST vs AVL por orden de inserción (TP4)
python algoritmos/experimentos/grafico_avl.py    # guarda docs/capturas/experimento-tp4.png
```

- Informe TP2 (secuencial vs binaria): [`docs/tp2-experimentos.md`](docs/tp2-experimentos.md)
- Informe TP3 (agrega el BST): [`docs/tp3-arbol-binario.md`](docs/tp3-arbol-binario.md)
- Informe TP4 (BST vs AVL y desbalance): [`docs/tp4-avl.md`](docs/tp4-avl.md)

## Documentación

| Doc | Contenido |
|---|---|
| [`docs/01-requerimientos.md`](docs/01-requerimientos.md) | Alcance, RF/RNF con estado estable, criterios de aceptación y observaciones |
| [`docs/02-casos-de-uso.md`](docs/02-casos-de-uso.md) | Diagrama general y 5 casos de uso textuales |
| [`docs/03-diagrama-clases.md`](docs/03-diagrama-clases.md) | Clases del dominio, `Catalogo`, `ArbolBinarioBusqueda` y `ArbolAVL` |
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
│   └── capturas/
├── modelos/
│   ├── lugar.py
│   └── salida.py
├── servicios/
│   └── catalogo.py          ← búsqueda secuencial, binaria, BST y AVL
├── estructuras/
│   ├── arbol_binario.py     ← TP3: NodoArbol y ArbolBinarioBusqueda
│   └── arbol_avl.py         ← TP4: NodoAVL y ArbolAVL
├── ui/
│   └── terminal.py          ← v2 (opción 5: estrategias · opción 6: BST vs AVL)
├── datos/
│   ├── lugares.json
│   ├── salidas.json
│   └── generar.py           ← TP2: datasets sintéticos (los generados están en .gitignore)
├── algoritmos/
│   └── experimentos/
│       ├── medicion.py      ← TP2 + TP3
│       ├── grafico.py
│       ├── medicion_avl.py  ← TP4
│       └── grafico_avl.py
└── tests/
    ├── test_catalogo.py
    ├── test_arbol_binario.py
    └── test_arbol_avl.py
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
