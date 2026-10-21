# Conexión entre estructuras

> Diagrama de flujo de datos del sistema. Se actualiza en cada TP con la
> estructura nueva.
>
> (El archivo se llama `04-diagrama-datos.md`, pero el contenido es la
> *conexión entre estructuras*: **el flujo de datos, no las clases.** Las
> clases van en [`03-diagrama-clases.md`](03-diagrama-clases.md).)

## Diagrama

```mermaid
graph LR
    subgraph Datos
        RAW["Datos crudos<br/>datos/lugares.json"] --> LISTA["Lista de lugares<br/>Catalogo._lugares"]
    end

    subgraph Estructuras
        LISTA --> ORD["Lista ordenada + arreglo de claves<br/>ordenar_por_titulo · TP2"]
        LISTA --> BST["Árbol BST por nombre normalizado<br/>ArbolBinarioBusqueda · TP3"]
        LISTA --> AVL["Árbol AVL por nombre normalizado<br/>ArbolAVL · TP4"]
        LISTA --> ARBCAT["Árbol general de categorías<br/>ArbolGeneral · TP5"]
        JER["Jerarquía de grupos<br/>datos/categorias.json"] --> ARBCAT
    end

    subgraph Busqueda
        LISTA --> S1["buscar<br/>secuencial · O(n)"]
        ORD --> S2["buscar_binaria<br/>binaria · O(log n)"]
        BST --> S3["buscar_arbol<br/>BST · O(log n)"]
        AVL --> S5["buscar_avl<br/>AVL · O(log n) garantizado"]
        BST --> S4["inorder<br/>listado alfabético"]
        ARBCAT --> S6["lugares_de_rama · ruta_de<br/>recorridos · O(n)"]
    end

    subgraph Servicio
        S1 --> CAT["Catalogo<br/>filtrar · buscar_parcial · listar"]
        S2 --> CAT
        S3 --> CAT
        S5 --> CAT
        S4 --> CAT
        S6 --> CAT
        LISTA --> CAT
    end

    CAT --> UI["Terminal v3<br/>opción 1 · 5 · 6 (BST vs AVL) · 7 (Explorar categorías)"]
```

## Qué aporta cada estructura

| Estructura | Qué resuelve | Por qué sigue existiendo |
|---|---|---|
| **Lista de lugares** | Recorridos lineales: `filtrar` por categoría, `buscar_parcial` (coincidencia parcial), `listar` en orden de carga | El BST **no** puede hacer búsqueda parcial: para eso hay que recorrerlo entero, O(n). La lista no se reemplaza, se complementa. |
| **Lista ordenada + `_claves`** | `buscar_binaria` en O(log n) | Es la estrategia del TP2. Se conserva como comparación y para catálogos que nunca mutan. |
| **Árbol BST** | `buscar_arbol` en O(log n) **y** inserción en O(log n) sin reordenar todo | La lista ordenada obliga a un `sort` de O(n log n) por cada lugar nuevo; el árbol inserta en O(log n) sin tocar el resto. |
| **Árbol AVL** | `buscar_avl` en **O(log n) garantizado** | Es el BST más rotaciones: mantiene la altura en O(log n) sin importar el orden de inserción, que es la debilidad que el BST del TP3 sí tiene. |
| **Árbol general de categorías** | Preguntar por un **grupo** ("Para comer"), navegar de lo general a lo específico y mostrar la ruta de un nodo | Ni la lista ni los árboles de búsqueda expresan jerarquía: `filtrar('Para comer')` devuelve 0. No acelera ninguna búsqueda (es O(n)): organiza, no indexa. |

## Dónde entra cada operación

1. **Carga**: `cargar_desde_json` arma la lista y llama a `indexar()`, que inserta
   cada lugar en el BST y en el AVL en orden de carga. `ordenar_por_titulo()` se
   llama aparte, cuando hace falta la binaria. (Para el AVL el orden de carga es
   indiferente: se rebalancea solo.)
2. **Búsqueda exacta** (opción 5 de la terminal): las **cuatro** estrategias reciben
   el mismo nombre, lo normalizan con `_normalizar` y devuelven la **misma
   instancia** de `Lugar` (o `None`).
3. **Búsqueda parcial** (opción 1): sigue siendo lineal sobre la lista, a propósito.
4. **Listado**: en orden de carga (la lista) o alfabético (el `inorder` del árbol).
5. **Demo del TP4** (opción 6): reconstruye BST y AVL con el mismo catálogo en orden
   alfabético para mostrar la degeneración del BST frente al AVL.
6. **Jerarquía** (opción 7, TP5): `indexar()` arma el árbol general a partir de la
   lista y de `datos/categorias.json` (cargado con `cargar_categorias_desde_json`).
   Cada `Lugar` cuelga como hoja de su categoría —la **misma instancia** que usan
   los demás índices— y `agregar_lugar()` lo mantiene al día.

Este diagrama muestra solo lo implementado. Las cuatro estrategias conviven: la
terminal ofrece las cuatro en la opción 5, y los recorridos que no son de búsqueda
exacta siguen yendo a la lista.
