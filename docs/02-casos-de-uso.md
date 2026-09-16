# Casos de uso — ¿Dónde vamos?

> Actualizado en TP1 con el formato de la consigna (Actor, Precondición, Flujo principal, Flujo alternativo).

## Caso de uso: Buscar lugar

- **Actor**: Usuario
- **Precondición**: el catálogo está cargado.
- **Flujo principal**:
  1. El usuario selecciona "Buscar lugar".
  2. El sistema pide el nombre del lugar.
  3. El usuario ingresa el nombre.
  4. El sistema lo busca (sin distinguir mayúsculas) y lo muestra.
- **Flujo alternativo**: si no se encuentra, el sistema informa que el lugar no existe.

## Caso de uso: Listar todos los lugares

- **Actor**: Usuario
- **Precondición**: el catálogo está cargado.
- **Flujo principal**:
  1. El usuario selecciona "Listar todos los lugares".
  2. El sistema recorre el catálogo completo.
  3. El sistema muestra todos los lugares.
- **Flujo alternativo**: si el catálogo está vacío, el sistema no muestra resultados.

## Caso de uso: Filtrar por categoría

- **Actor**: Usuario
- **Precondición**: el catálogo está cargado.
- **Flujo principal**:
  1. El usuario selecciona "Filtrar por categoría".
  2. El sistema pide una categoría.
  3. El usuario ingresa la categoría (ej. parrilla, bar, cafeteria).
  4. El sistema muestra solo los lugares de esa categoría (sin distinguir mayúsculas).
- **Flujo alternativo**: si no hay lugares en esa categoría, el sistema lo informa.

## Caso de uso: Ver participantes por salida

- **Actor**: Usuario
- **Precondición**: el catálogo y las salidas están cargados.
- **Flujo principal**:
  1. El usuario selecciona "Ver participantes por salida".
  2. El sistema recorre las salidas cargadas.
  3. Para cada salida muestra su nombre y la lista de participantes.
- **Flujo alternativo**: si no hay salidas cargadas, el sistema no muestra resultados.

---

Casos pendientes de implementar (TPs siguientes):

## Caso de uso (futuro): Ver Top 10

- **Actor**: Usuario
- **Objetivo**: consultar los diez lugares mejor valorados.
- **Nota**: se implementa cuando entren las estructuras de ordenamiento (heap).

## Caso de uso (futuro): Recibir sugerencias

- **Actor**: Usuario
- **Objetivo**: obtener lugares compatibles con las preferencias, las fechas y el presupuesto del grupo.
- **Nota**: se implementa cuando entren los grafos/relaciones entre lugares.