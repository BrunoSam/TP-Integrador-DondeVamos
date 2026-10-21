# Casos de uso — ¿Dónde vamos?

> Actualizado en TP5. Formato de la consigna: Actor, Precondición, Flujo
> principal, Flujo alternativo, Postcondición.

## Diagrama general

```mermaid
graph TD
    U(("Usuario<br/>(grupo de amigos<br/>que planea una salida)"))
    U -->|"1"| CU1["Buscar lugar<br/>(coincidencia parcial)"]
    U -->|"2"| CU2["Listar lugares"]
    U -->|"3"| CU3["Filtrar por categoría"]
    U -->|"4"| CU4["Ver participantes por salida"]
    U -->|"5"| CU5["Buscar por nombre exacto<br/>comparando estrategias"]
    U -->|"7"| CU8["Explorar categorías<br/>(árbol general)"]
    U -->|"⏳ TP6"| CU6["Ver Top 10"]
    U -->|"⏳ TP7+"| CU7["Ver lugares relacionados"]
```

El actor es **una sola persona**: el usuario objetivo definido en TP0 (una pareja
o un grupo pequeño de amigos). No hay administradores ni otros actores.

---

## Caso de uso: Buscar lugar (parcial)

- **Actor**: Usuario
- **Precondición**: el catálogo está cargado.
- **Flujo principal**:
  1. El usuario selecciona "Buscar lugar".
  2. El sistema pide el nombre o parte del nombre.
  3. El usuario ingresa el texto.
  4. El sistema busca las coincidencias parciales (sin distinguir mayúsculas ni tildes).
  5. El sistema muestra todos los lugares encontrados.
- **Flujo alternativo**: si no hay coincidencias, el sistema informa que no encontró nada.
- **Postcondición**: el usuario vio los datos de los lugares encontrados. El catálogo no se modifica.

## Caso de uso: Listar todos los lugares

- **Actor**: Usuario
- **Precondición**: el catálogo está cargado.
- **Flujo principal**:
  1. El usuario selecciona "Listar todos los lugares".
  2. El sistema pregunta en qué orden.
  3. El usuario elige orden de carga (la lista) u orden alfabético (recorrido inorder del árbol).
  4. El sistema muestra el catálogo completo en el orden elegido.
- **Flujo alternativo**: si el catálogo está vacío, el sistema avisa que no hay lugares.
- **Postcondición**: el usuario recorrió el catálogo. Ninguna estructura se modifica.

## Caso de uso: Filtrar por categoría

- **Actor**: Usuario
- **Precondición**: el catálogo está cargado.
- **Flujo principal**:
  1. El usuario selecciona "Filtrar por categoría".
  2. El sistema pide una categoría.
  3. El usuario ingresa la categoría (ej. parrilla, bar, cafeteria).
  4. El sistema muestra solo los lugares de esa categoría (sin distinguir mayúsculas).
- **Flujo alternativo**: si no hay lugares en esa categoría, el sistema lo informa.
- **Postcondición**: el usuario vio los lugares de la categoría indicada.

## Caso de uso: Ver participantes por salida

- **Actor**: Usuario
- **Precondición**: el catálogo y las salidas están cargados.
- **Flujo principal**:
  1. El usuario selecciona "Ver participantes por salida".
  2. El sistema recorre las salidas cargadas.
  3. Para cada salida muestra su nombre y la lista de participantes.
- **Flujo alternativo**: si no hay salidas cargadas, el sistema no muestra resultados.
- **Postcondición**: el usuario vio quién asiste a cada salida.

## Caso de uso: Buscar por nombre exacto comparando estrategias

- **Actor**: Usuario
- **Precondición**: el catálogo está cargado e indexado.
- **Objetivo**: encontrar un lugar por nombre completo y ver cómo lo resuelven las cuatro estructuras de búsqueda.
- **Flujo principal**:
  1. El usuario selecciona "Buscar por nombre exacto (comparar estrategias)".
  2. El sistema pide el nombre completo del lugar.
  3. El usuario elige con qué estrategia buscar: secuencial, binaria, árbol BST, árbol AVL, o las cuatro.
  4. El sistema normaliza el nombre (minúsculas, sin tildes) y ejecuta la búsqueda elegida.
  5. El sistema muestra el lugar encontrado y el tiempo que tardó cada estrategia.
- **Flujo alternativo**: si el nombre no existe, cada estrategia informa que no lo encontró y devuelve `None`.
- **Postcondición**: el usuario vio el lugar y el tiempo de cada estrategia. Si usó la binaria, el catálogo quedó ordenado alfabéticamente (es el requisito de `buscar_binaria`).

## Caso de uso: Explorar categorías

- **Actor**: Usuario
- **Precondición**: el catálogo y la jerarquía de categorías están cargados.
- **Objetivo**: encontrar un lugar yendo de lo general a lo específico (comer, tomar algo…) en vez de saber su nombre o su categoría exacta.
- **Flujo principal**:
  1. El usuario selecciona "Explorar categorías" y elige "Navegar la jerarquía".
  2. El sistema muestra dónde está el usuario (la ruta desde la raíz) y los elementos de ese nivel, con la cantidad de lugares de cada rama.
  3. El usuario elige un número para entrar a un grupo o categoría, o `0` para subir un nivel.
  4. Al llegar a una categoría, el sistema lista sus lugares con la puntuación; al elegir uno muestra todos sus datos.
- **Flujos alternativos**:
  - *Ver lugares de una rama*: el usuario indica un grupo o categoría (sin distinguir tildes ni mayúsculas) y el sistema muestra todos los lugares de esa rama, a cualquier profundidad.
  - *Buscar en el árbol*: el usuario ingresa un texto y el sistema muestra la ruta completa de cada nodo cuyo nombre lo contiene.
  - *Ver recorridos*: el sistema muestra los grupos y categorías en preorden, postorden y por niveles, desde la raíz o desde una rama elegida.
  - Si el nombre no existe, el sistema lo informa. Si la opción de navegación no es válida, la rechaza y vuelve a preguntar.
- **Postcondición**: el usuario vio los lugares de la rama elegida. Ninguna estructura se modifica.

---

## Casos pendientes de implementar (TPs siguientes)

## Caso de uso (futuro): Ver Top 10

- **Actor**: Usuario
- **Objetivo**: consultar los diez lugares mejor valorados.
- **Nota**: se implementa cuando entren las estructuras de ordenamiento (heap, TP6).

## Caso de uso (futuro): Recibir sugerencias

- **Actor**: Usuario
- **Objetivo**: obtener lugares compatibles con las preferencias, las fechas y el presupuesto del grupo.
- **Nota**: se implementa cuando entren los grafos/relaciones entre lugares (TP7+).
