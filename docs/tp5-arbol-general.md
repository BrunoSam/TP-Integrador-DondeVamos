# TP5 — Árbol general: organizá tu universo

> Informe del TP5. Todo lo que se cita acá (salidas, conteos, alturas) sale de
> correr el código del repositorio; no hay tiempos medidos porque este TP no
> compara velocidades (ver §8).

## 1. El problema: la lista plana no tiene jerarquía

Hasta el TP4 el catálogo era una lista de lugares con un campo `categoria`
(`parrilla`, `bar`, `cafeteria`…). Con eso `filtrar` responde "dame las
parrillas", pero no puede responder lo que un grupo de amigos realmente pregunta:

> *"Queremos **comer** algo. ¿Qué hay?"*

"Comer" no es una categoría del dato: es un **grupo** que junta parrilla,
restaurante, bodegón y pizzería. Lo comprobamos:

```text
lugares_de_rama('Para comer') -> 20 lugares
filtrar('Para comer')         -> 0 lugares
```

La jerarquía natural del dominio es un árbol, y como cada nodo puede tener
cualquier cantidad de hijos (un grupo tiene 4 categorías, otro tiene 1) no sirve
un árbol binario: hace falta un **árbol general (n-ario)**.

## 2. La jerarquía que elegimos

```text
Dónde vamos (50 lugares)
├── Para comer (20 lugares)
│   ├── Parrilla (5 lugares)
│   ├── Restaurante (5 lugares)
│   ├── Bodegón (5 lugares)
│   └── Pizzería (5 lugares)
├── Para tomar algo (25 lugares)
│   ├── Bar (15 lugares)
│   └── Cafetería (10 lugares)
└── Algo dulce (5 lugares)
    └── Heladería (5 lugares)
```

Con los 50 lugares como hojas, el árbol tiene **61 nodos** (1 raíz + 3 grupos +
7 categorías + 50 lugares) y **altura 4**. Es el mismo esquema de la consigna
(Películas > Ciencia ficción > Cyberpunk) aplicado a nuestro dominio.

Tres decisiones de diseño:

1. **Los lugares son las hojas.** Así el árbol responde "qué hay bajo esta rama"
   con las hojas del subárbol, y un grupo vacío o una categoría sin lugares
   siguen siendo nodos válidos.
2. **La jerarquía es un dato, no código.** Vive en `datos/categorias.json`
   (`{"raiz": ..., "grupos": {grupo: [categorías]}}`). Cambiar "Para comer" por
   otro agrupamiento no toca Python.
3. **Ningún lugar queda afuera.** Si un lugar trae una categoría que la
   jerarquía no conoce, el catálogo la crea bajo un grupo **"Otros"**. Sin
   archivo de jerarquía cargado, las categorías cuelgan directo de la raíz: el
   árbol existe igual y se arma solo con los datos.

Las categorías se enganchan **sin distinguir tildes ni mayúsculas** (usa la misma
`_normalizar` de todo el proyecto): el JSON dice `"Cafetería"` y los lugares
dicen `"cafeteria"`.

## 3. Qué implementamos

`estructuras/arbol_general.py`, con el mismo criterio que el BST y el AVL: **no
conoce el dominio**. La función `clave` se inyecta como `callable`; el catálogo le
pasa `_normalizar`.

| Clase | Responsabilidad |
|---|---|
| `NodoGeneral` | Etiqueta, valor opcional, **padre** y lista de hijos. `hijos` se expone como tupla para que nadie modifique el árbol desde afuera. |
| `ArbolGeneral` | Raíz única, alta/baja de nodos, tres recorridos, dos búsquedas, ruta, nivel, altura y dibujo. |

El **padre** se guarda en cada nodo (el BST no lo necesitaba). Con él la ruta de
un nodo y la navegación "subir un nivel" cuestan O(h) sin recorrer el árbol.

### 3.1 Operaciones y complejidad

`n` = nodos del árbol, `h` = altura.

| Operación | Qué hace | Costo |
|---|---|---|
| `agregar(padre, etiqueta, valor)` | Cuelga un hijo nuevo | O(h) (verificar que el padre es del árbol) |
| `eliminar(nodo)` | Borra el nodo y todo su subárbol | O(subárbol) |
| `preorden` / `postorden` / `por_niveles` | Recorridos, opcionalmente desde un subárbol | O(n) |
| `buscar(texto)` | Primer match **por niveles** (BFS) | O(n) |
| `buscar_profundidad(texto)` | Primer match **en preorden** (DFS) | O(n) |
| `buscar_todos(texto)` | Todos los nodos que contienen el texto | O(n) |
| `camino(nodo)` / `nivel(nodo)` | Ruta desde la raíz / nivel (raíz = 1) | O(h) |
| `hojas(desde)` | Las hojas de un subárbol | O(subárbol) |
| `altura()` | Niveles del camino más largo | O(n) |
| `dibujar(desde, max_nivel, formato)` | El árbol como texto con ramas | O(líneas × h) |

Notas de diseño:

- **Todo es iterativo**, igual que el BST del TP3. Una jerarquía en cadena
  profunda reventaría el límite de recursión de Python (~1000); hay un test con
  una cadena de 3.000 niveles que lo fija. A diferencia del AVL, un árbol general
  **no tiene altura acotada**, así que no se puede asumir que la recursión sea
  segura.
- **Los niveles se cuentan desde 1**, igual que `altura()` en los otros árboles.
  Así `altura()` es exactamente el mayor nivel que existe.
- **`altura()` no se cachea:** se calcula con un recorrido por niveles. El AVL
  la guardaba en el nodo porque la necesitaba en cada inserción; acá solo se
  consulta al mostrar, y mantenerla al día en cada alta/baja no se justifica.

## 4. Los recorridos, con ejemplos

Primero sobre el árbol **de la consigna** (la salida real de
`python algoritmos/experimentos/ejemplo_recorridos.py`):

```text
Películas
├── Ciencia ficción
│   ├── Cyberpunk
│   ├── Viajes temporales
│   └── Inteligencia artificial
├── Acción
└── Comedia

Preorden    : Películas → Ciencia ficción → Cyberpunk → Viajes temporales → Inteligencia artificial → Acción → Comedia
Postorden   : Cyberpunk → Viajes temporales → Inteligencia artificial → Ciencia ficción → Acción → Comedia → Películas
Por niveles : Películas → Ciencia ficción → Acción → Comedia → Cyberpunk → Viajes temporales → Inteligencia artificial
```

| Recorrido | Regla | Para qué sirve en el catálogo |
|---|---|---|
| **Preorden** | El padre antes que sus hijos | Leer la jerarquía como un índice, de arriba hacia abajo |
| **Postorden** | Los hijos antes que su padre | Procesar primero lo específico: es el orden para contar o borrar de abajo hacia arriba |
| **Por niveles (BFS)** | Todo un nivel antes del siguiente | Ir de lo general a lo específico: primero los grupos, después las categorías |

Y sobre los grupos y categorías **reales** (sin los 50 lugares, que son hojas):

```text
preorden  : Dónde vamos → Para comer → Parrilla → Restaurante → Bodegón → Pizzería → Para tomar algo → Bar → Cafetería → Algo dulce → Heladería
postorden : Parrilla → Restaurante → Bodegón → Pizzería → Para comer → Bar → Cafetería → Para tomar algo → Heladería → Algo dulce → Dónde vamos
niveles   : Dónde vamos → Para comer → Para tomar algo → Algo dulce → Parrilla → Restaurante → Bodegón → Pizzería → Bar → Cafetería → Heladería
```

Cómo se resolvió cada uno sin recursión:

- **Preorden:** una pila; los hijos se apilan **al revés** para que el primero
  salga primero.
- **Postorden:** la misma pila pero apilando los hijos en orden, y al final se
  **invierte** el resultado (el mismo truco que usa el BST del TP3).
- **Por niveles:** se avanza con una lista "frontera" que se reemplaza por los
  hijos de todos sus nodos. Como subproducto, `niveles()` entrega los nodos ya
  agrupados por nivel y `altura()` es su longitud.

## 5. Las búsquedas

Hay dos preguntas distintas y por eso dos búsquedas:

- **Exacta** (`buscar`, `buscar_profundidad`): devuelve un nodo. Se diferencian
  cuando una etiqueta se repite a distinta profundidad. Con "Clásicos" bajo
  *Cyberpunk* (nivel 4) y también directo bajo la raíz (nivel 2):

  ```text
  buscar (por niveles, BFS)     -> nivel 2
  buscar_profundidad (DFS)      -> nivel 4
  ```

  BFS devuelve el más **cercano** a donde se busca; DFS el primero **en orden de
  lectura**. En el catálogo se usa BFS (`buscar_nodo`): si un lugar se llamara
  igual que una categoría, gana la categoría, que está más arriba.
- **Parcial** (`buscar_todos`): todos los nodos cuyo nombre *contiene* el texto,
  con la ruta de cada uno. `"cafe"` encuentra la categoría Cafetería y los
  lugares que tienen "cafe" en el nombre.

## 6. Cómo lo integramos

### 6.1 En el catálogo

`Catalogo` **suma** el árbol; no reemplaza nada (misma política que con el BST y
el AVL). `indexar()` ahora también arma la jerarquía, y `agregar_lugar()` cuelga
el lugar nuevo en su categoría, así que no hace falta reindexar.

| Método | Qué devuelve |
|---|---|
| `cargar_categorias_desde_json(ruta)` | Carga la jerarquía y rearma el árbol |
| `arbol_categorias` | El `ArbolGeneral` (para navegar) |
| `explorar_categorias(incluir_lugares=False)` | El árbol como líneas de texto |
| `buscar_nodo(texto)` / `buscar_nodos(texto)` | Un nodo exacto / todos los que contienen el texto |
| `ruta_de(nodo)` | `"Dónde vamos > Para comer > Parrilla > Don Julio Parrilla"` |
| `lugares_de(nodo)` / `lugares_de_rama(texto)` | Los lugares bajo una rama (`None` si el nombre no existe) |
| `recorrer_categorias(orden, desde)` | Etiquetas de grupos y categorías en preorden, postorden o por niveles |
| `describir_nodo(nodo)` | `"Parrilla (5 lugares)"` o `"Don Julio Parrilla (⭐ 4.4)"` |

La terminal no recorre el árbol por su cuenta para decidir qué es un lugar: le
pide todo eso al catálogo. Solo usa `nodo.hijos` y `nodo.padre` para navegar.

### 6.2 En la terminal (versión 3)

La opción **7 — Explorar categorías** abre un submenú:

```text
--- EXPLORAR CATEGORÍAS ---
1. Navegar la jerarquía (entrar y subir de nivel)
2. Ver el árbol de categorías
3. Ver el árbol completo (con los lugares)
4. Buscar en el árbol y ver su ruta
5. Ver los lugares de una rama (ej: todo "Para comer")
6. Recorridos: preorden, postorden y por niveles
0. Volver al menú principal
```

La navegación (opción 1) se baja eligiendo un número y se sube con `0`:

```text
Estás en: Dónde vamos > Para comer
  1. Parrilla (5 lugares)
  2. Restaurante (5 lugares)
  3. Bodegón (5 lugares)
  4. Pizzería (5 lugares)
  0. Subir un nivel
Elegí: 1

Estás en: Dónde vamos > Para comer > Parrilla
  1. Parrilla Sanabria Palermo (⭐ 4.8)
  2. Don Julio Parrilla (⭐ 4.4)
  ...
```

Al elegir un lugar se muestran sus datos y se sigue en la misma rama.

## 7. Pruebas

Se agregaron **87 pruebas** (la suite pasó de 112 a **199**):

| Archivo | Qué fija |
|---|---|
| `tests/test_arbol_general.py` (45) | Estructura, los tres recorridos con el árbol exacto de la consigna, BFS vs DFS, ruta/nivel/altura, eliminación, dibujo, y una cadena de 3.000 niveles sin recursión |
| `tests/test_catalogo_categorias.py` (34) | Armado de la jerarquía, grupo "Otros", categorías nuevas, altas incrementales, consultas por rama, y el **dataset real**: los 50 lugares están en el árbol, sin repetir, y cada categoría coincide con `filtrar` |
| `tests/test_terminal_categorias.py` (8) | Navegación, rama inexistente, búsqueda con ruta y recorridos, con `input` simulado |

Una prueba cruza el árbol con la lista: para cada categoría real,
`lugares_de_rama(categoria)` devuelve **los mismos lugares** que `filtrar`. Es la
garantía de que el árbol y la lista no se contradicen.

## 8. La lectura honesta: qué aporta y qué no

- **El árbol no acelera nada.** `buscar` es O(n), igual que la búsqueda
  secuencial del TP1. No hay medición de tiempos en este TP a propósito: el árbol
  general no compite con el BST ni con `bisect`, porque no es un índice de
  búsqueda. Su aporte es **semántico**: expresa que "Para comer" *contiene*
  parrilla, restaurante, bodegón y pizzería, algo que la lista plana no puede
  decir.
- **Un nodo tiene un solo padre.** "Cafetería" podría ir tanto en *Para tomar
  algo* como en *Algo dulce*, pero en un árbol solo puede estar en un lugar. Es
  una limitación de la estructura, no del código, y es la motivación natural del
  **grafo del TP7** (relaciones que no son jerárquicas).
- **La jerarquía no indexa la zona.** Buscar `"almagro"` en el árbol no
  encuentra nada: el árbol conoce nombres de grupos, categorías y lugares, no
  sus zonas. Para eso sigue valiendo `buscar_parcial`.
- **La búsqueda exacta es lineal.** Con 61 nodos es irrelevante; con una
  jerarquía de cientos de miles habría que indexar nombres aparte (un diccionario
  o el AVL del TP4). No lo hicimos porque el árbol de categorías es chico por
  naturaleza: los lugares son hojas y las categorías son pocas.
- **`dibujar` imprime prefijos de ancho proporcional a la profundidad**, así que
  dibujar una cadena de miles de niveles gasta memoria cuadrática. No es un caso
  realista para una jerarquía de categorías, y `max_nivel` lo acota.
- **Eliminar existe en el árbol, no en el catálogo.** `ArbolGeneral.eliminar`
  está implementado y probado, pero el catálogo no expone borrar lugares (ni
  tampoco lo hace con la lista ni con el BST/AVL), así que borrar de un solo
  lado dejaría las estructuras inconsistentes. Queda como extensión.
- **Los lugares del árbol conservan el orden de carga.** Los que se agregan
  después quedan al final de su categoría; no se reordenan alfabéticamente.

## 9. Conclusión

El árbol general cubre un hueco que ninguna estructura anterior cubría: la
**jerarquía**. El BST y el AVL ordenaban por nombre para buscar rápido; el árbol
general organiza por significado para **explorar**. Por eso conviven en el mismo
`Catalogo` sin pisarse: tres formas de ver los mismos 50 objetos `Lugar`
(lista, índice por nombre, jerarquía de categorías).

La decisión de diseño que más pesó fue mantener la estructura **genérica**
(`clave` inyectada, sin importar nada del dominio) y llevar la jerarquía a un
archivo de datos. El resultado es que el mismo `ArbolGeneral` representa tanto el
árbol de películas de la consigna como las categorías de lugares.

## Reproducción

```bash
python algoritmos/experimentos/ejemplo_recorridos.py   # recorridos y búsquedas (consigna + catálogo real)
python main.py                                         # opción 7: Explorar categorías
python -m unittest tests.test_arbol_general tests.test_catalogo_categorias tests.test_terminal_categorias
```
