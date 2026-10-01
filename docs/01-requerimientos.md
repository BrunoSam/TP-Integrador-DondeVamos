# Requerimientos — ¿Dónde vamos?

> Estado: TP3. Se actualiza en cada etapa con lo que se implementa.
> Los IDs (`RFxx` / `RNFxx`) son estables: en la defensa se citan tal cual.

## Alcance

El sistema permite buscar, listar y filtrar lugares (cafés, restaurantes, bares,
heladerías, etc.) de CABA para que una pareja o un grupo pequeño de amigos pueda
elegir dónde salir, considerando categoría, zona, puntuación, costo y horario.
Está pensado para una pareja o un grupo pequeño de amigos que quiere organizar una
salida o escapada y necesita encontrar un lugar que se adapte a sus preferencias y
al presupuesto disponible.

### Contexto del TP0

**Dominio: Salidas / Turismo.** El dominio permite trabajar con datos de lugares,
categorías, valoraciones, costos y preferencias. Estos datos pueden obtenerse
mediante datasets públicos, fuentes publicables o datos de prueba realistas.

El problema que motiva el proyecto es que cuando el grupo planeaba salidas, a veces
no se les ocurrían buenos lugares y terminaban repitiendo los mismos o perdiendo
tiempo discutiendo. Lo que buscamos es facilitar que la gente pase un buen momento
en pareja o entre amigos, porque lo importante no es el lugar en sí, sino los
momentos que se comparten y lo que uno recuerda después. Contar con datos propios
nos permite iterar sin depender de servicios externos y trabajar sobre un caso de
uso cercano al que realmente necesitamos resolver.

### Estado de avance

| TP | Qué se implementó | Documentos actualizados |
|---|---|---|
| TP0 | Propuesta, repo, tablero, bocetos | 01 (borrador), 03 (boceto), 05 (tablero), README |
| TP1 | Modelo de dominio, catálogo, terminal v1, 14 pruebas | 01, 02, 03, 05, README |
| TP2 | Segunda estrategia de búsqueda (binaria) + experimentos | 01, 04, 05, `docs/tp2-experimentos.md`, README |
| TP3 | Árbol binario de búsqueda integrado al catálogo, terminal v2 | 01, 02, 03, 04, 05, `docs/tp3-arbol-binario.md`, README |

## Requerimientos funcionales (RF)

| ID | Requerimiento | Estado |
|---|---|---|
| RF01 | El sistema debe permitir buscar un lugar por nombre | ✅ TP1 (secuencial) · ✅ TP2 (binaria) · ✅ TP3 (BST) |
| RF02 | El sistema debe permitir listar lugares según una categoría | ✅ TP1 |
| RF03 | El sistema debe mostrar el Top 10 de lugares mejor valorados | ⏳ TP6 (heap) |
| RF04 | El sistema debe mostrar lugares relacionados con un lugar dado | ⏳ TP7 (grafo) |
| RF05 | El sistema debe sugerir lugares a partir de las preferencias, la cantidad de personas, las fechas y el presupuesto del grupo | ⏳ TP10 |
| RF06 | El sistema debe permitir ver los participantes de cada salida | ✅ TP1 |
| RF07 | El sistema debe permitir listar todos los lugares en orden alfabético | ✅ TP3 (recorrido inorder del BST) |

> **Alcance real a hoy:** búsqueda (RF01), filtrado (RF02), participantes (RF06) y
> listado (RF07). El Top 10 (RF03) sigue pendiente: aparece en la propuesta del TP0
> pero no se implementó, porque necesita una estructura de ordenamiento por
> prioridad, que es exactamente lo que trae el heap del TP6. Preferimos dejarlo
> explícitamente pendiente antes que simularlo con un `sorted()` sobre 50 lugares.
> Los relacionados (RF04) necesitan el grafo del TP7 y las sugerencias (RF05) el
> producto final.

### Criterios de aceptación

> **RF01 — Búsqueda por nombre**
> - Devuelve el `Lugar` cuyo nombre coincide con el buscado, o `None` si no existe.
> - No distingue mayúsculas, minúsculas ni tildes: `"LA BIELA"`, `"la biela"` y `"La Biela"` devuelven lo mismo; `"gastronomía"` encuentra `"Gastronomia"`. Ojo: no recorta espacios sobrantes, eso no está implementado.
> - Con 100.000 lugares responde en menos de 0,03 ms por búsqueda (medido: 0,0060 ms binaria y 0,0205 ms BST).
> - Ofrece las tres estrategias (secuencial, binaria, BST) y cronometra cada una; las tres devuelven el mismo resultado.

> **RF02 — Filtrar por categoría**
> - Devuelve todos los lugares de la categoría indicada.
> - No distingue mayúsculas: `"PARRILLA"` y `"parrilla"` devuelven lo mismo.
> - Si la categoría no existe, informa que no encontró resultados.

> **RF03 — Top 10**
> - Muestra exactamente 10 lugares, o todos los que existan si son menos.
> - Orden descendente por puntuación, desempate alfabético por nombre.
> - Responde en menos de 1 segundo con 10.000 lugares.

> **RF06 — Participantes de una salida**
> - Muestra el nombre de cada salida con la lista de participantes.
> - Si no hay salidas cargadas, avisa que no hay resultados.

> **RF07 — Listado alfabético**
> - Devuelve todos los lugares ordenados por nombre normalizado.
> - No duplica ni pierde lugares: la cantidad devuelta es igual a la del catálogo.
> - Con 2.000 lugares insercionalmente ordenados (peor caso) no revienta por recursión.

## Requerimientos no funcionales (RNF)

| ID | Requerimiento | Verificación | Estado |
|---|---|---|---|
| RNF01 | La búsqueda debe mantener un tiempo de respuesta aceptable con un volumen superior a 1.000 lugares | TP2 + TP3 (`docs/tp2-experimentos.md`, `docs/tp3-arbol-binario.md`) | ✅ con salvedad |
| RNF02 | El sistema debe soportar al menos 10.000 lugares sin degradar perceptiblemente la respuesta | TP2 (experimentos) | ✅ |
| RNF03 | La interfaz debe ser usable por alguien que no conoce la implementación | Demo de la terminal | ✅ |
| RNF04 | El proyecto debe ejecutarse con Python 3.10+ sin instalaciones extra | README | ✅ |

> **Salvedad del RNF01:** se cumple con la búsqueda binaria y con el BST siempre que
> el árbol no haya degenerado. El BST **no garantiza** O(log n): con inserciones
> ordenadas la altura es n y la búsqueda vuelve a ser O(n). Está documentado en
> `docs/tp3-arbol-binario.md` §9 y es el motivo del AVL del TP4. No queremos reportar
> este RNF como cumplido sin ese matiz.

## Ejemplo de uso (input/output)

```text
=============================================
   🌳 ¿DÓNDE VAMOS? — TERMINAL (v2)
=============================================
1. Buscar lugar (coincidencia parcial)
2. Listar todos los lugares
3. Filtrar por categoría
4. Ver participantes por salida
5. Buscar por nombre exacto (comparar estrategias)
0. Salir
---------------------------------------------
Opción: 5
Nombre exacto: la biela

Estrategias:
  1) Secuencial  O(n)
  2) Binaria     O(log n)
  3) Arbol BST   O(log n)
  4) Las tres
Estrategia: 4

--- Secuencial (O(n)) ---
  La Biela — cafeteria (Recoleta) [⭐ 4.2 | $ | 08:00-00:00]
  Tiempo: 0.09440 ms

--- Binaria (O(log n)) ---
  La Biela — cafeteria (Recoleta) [⭐ 4.2 | $ | 08:00-00:00]
  Tiempo: 0.01730 ms

--- Arbol BST (O(log n)) ---
  La Biela — cafeteria (Recoleta) [⭐ 4.2 | $ | 08:00-00:00]
  Tiempo: 0.01300 ms
```

## Fuera de alcance (por ahora)

- No se implementan autenticación ni perfiles de usuario.
- No se realiza persistencia de preferencias entre ejecuciones.
- No se realizan reservas ni pagos.
- No se integran servicios externos de reservas.
- No se implementan recomendaciones mediante IA generativa.

## Observaciones

- **La lista no se reemplaza, se complementa.** El BST resuelve la búsqueda exacta
  y el listado alfabético (RF01, RF07), pero `filtrar` y la búsqueda parcial siguen
  siendo lineales sobre la lista a propósito: el BST no puede responder una
  coincidencia parcial en O(log n), habría que recorrerlo entero.
- **La clave del árbol es el nombre normalizado**, la misma que ya usaban las dos
  estrategias del TP2. Elegir otra clave (por ejemplo `puntuacion`) habría roto la
  comparabilidad con el TP2 y no resolvería la consulta del usuario. Ver
  `docs/tp3-arbol-binario.md` §2.
- **Medimos a favor de la estructura que comparamos.** La sonda del TP2
  (`"Lugar {n-1}"`) resultó ser el peor caso de las tres estrategias a la vez. En
  el TP3 la conservamos por comparabilidad y agregamos una sonda `medio`, para no
  presentar al BST solo en su peor caso.
- **El BST no le ganó a `bisect`.** Con 100.000 lugares la binaria responde en
  0,0060 ms y el árbol en 0,0205 ms, porque `bisect` es código C y el árbol camina
  ~50 nodos en Python interpretado. Lo dejamos escrito tal cual en el informe: el
  árbol aporta inserción en O(log n) sin reordenar, no velocidad en la búsqueda.
- **RF03 está declarado pero no implementado.** Es una decisión consciente, no un
  olvido; ver "Alcance real a hoy".
