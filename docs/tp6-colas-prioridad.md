# TP6 — Colas de prioridad (Heap Binario) / Top-N

## Objetivo
Obtener el Top-N de lugares eficientemente usando una cola de prioridad. Implementar el heap binario **manual** con indexación **1-based**, sin usar `heapq`.

## Reglas de cátedra aplicadas
- **Indexación 1-based**: raíz en `A[1]`, variable `n` para cantidad actual.
- **Navegación**: hijo izquierdo `2*i`, hijo derecho `2*i+1`, padre `floor(i/2)`.
- **Árbol binario completo**: se llena de izquierda a derecha.
- **Max-Heap**: `A[padre] >= A[hijo]`, la raíz contiene el elemento máximo.
- **Inserción**: agregar al final `A[n+1]`, `n++`, flotar con **_subir (sift-up)**. O(log n).
- **Eliminar raíz**: guardar `A[1]`, mover último a raíz, `n--`, hundir con **_bajar (sift-down)**. O(log n).

## Función de prioridad
Se usa como clave primaria **`lugar.puntuacion`** (mayor puntuación = mayor prioridad). 
Para asegurar un ranking **determinista** en caso de empate se usa **`nombre` normalizado** como desempate.

## ¿Por qué heap y no `sorted()`?
Si ordenáramos todo el dataset con `sorted(self._lugares, key=lambda x: x.puntuacion, reverse=True)[:n]` sería **O(m log m)** donde `m` es el total de elementos. 
Con un heap binario:
- Construimos/insertamos los elementos en **O(m log m)** en el peor caso con inserciones, o se puede pensar en operar por elemento.
- Para obtener **Top-N** extraemos N veces desde la raíz en **O(n log m)**.
- Si el catálogo es **dinámico** (se agregan lugares), mantener un heap resulta más natural para una **cola de prioridad** que reordenar toda la lista cada vez.
- Además se demuestra el uso de la estructura pedida por la cátedra.

## Integración
- `estructuras/heap_binario.py`: implementación manual sin `heapq`.
- `servicios/catalogo.py`: `obtener_top_n(n, clave_prioridad=None)` construye un max-heap con los lugares y devuelve los primeros N elementos.
- `ui/terminal.py` (v4): opción **8. Ver Top N recomendaciones**.
- `tests/test_heap_binario.py`: pruebas del heap y del Top-N.

## Ejemplo
```text
--- TOP 5 ---
1. Pizza Franca | Horno Napoletano — ...
2. Icaro Cocktail Bar — ...
...
```