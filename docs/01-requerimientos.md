# ¿Dónde vamos? — Propuesta (TP0)

Sistema de recomendación y organización de salidas que permite buscar, comparar y descubrir lugares y actividades considerando las preferencias, las fechas y el presupuesto de un grupo de personas.

## 1. Dominio elegido y justificación

**Dominio: Salidas / Turismo.**

El dominio permite trabajar con datos de lugares (cafés, restaurantes, miradores, trekkings, actividades culturales), categorías, valoraciones, costos y preferencias. Estos datos pueden obtenerse mediante datasets públicos, fuentes publicables o datos de prueba realistas.

El problema que motiva el proyecto es que cuando el grupo planeaba salidas, a veces no se les ocurrían buenos lugares y terminaban repitiendo los mismos o perdiendo tiempo discutiendo. Lo que buscamos es facilitar que la gente pase un buen momento en pareja o entre amigos, porque lo importante no es el lugar en sí, sino los momentos que se comparten y lo que uno recuerda después. Por eso necesitamos un sistema que, en base a gustos, fechas y presupuesto, sugiera opciones concretas y permita enfocarse en lo que realmente importa: disfrutar juntos. Contar con datos propios nos permite iterar sin depender de servicios externos y trabajar sobre un caso de uso cercano a lo que realmente necesitamos resolver.

## 2. Problema que resuelve

Una pareja o un grupo de amigos quiere organizar una salida, pero tiene dificultades para decidir dónde ir porque cada integrante puede tener preferencias y un presupuesto diferente.

## 3. Usuario objetivo

Una pareja o un grupo pequeño de amigos que quiere organizar una salida o escapada y necesita encontrar un lugar que se adapte a sus preferencias y al presupuesto disponible.

## 4. Funcionalidades iniciales

| ID | Funcionalidad |
|---|---|
| F1 | Buscar un lugar por nombre |
| F2 | Listar lugares según una categoría |
| F3 | Ver el Top 10 de lugares mejor valorados |
| F4 | Ver lugares relacionados con uno dado |
| F5 | Sugerir lugares a partir de las preferencias del grupo |

F1, F2 y F3 (parcial) se implementan en la v1 del TP1; F4 y F5 se agregan a partir de TP3+.

## 5. Ejemplo de uso (input/output)

```text
==============================================
   🌳 ¿DÓNDE VAMOS? — TERMINAL (v1)
==============================================
1. Buscar lugar
2. Listar todos los lugares
3. Filtrar por categoría
4. Ver participantes por salida
0. Salir
----------------------------------------------
Opción: 1
Nombre a buscar: La Biela

--- RESULTADOS ---

La Biela — cafeteria (Recoleta) [⭐ 4.2 | $ | 08:00-00:00]
```

## 6. Requerimientos (borrador)

> Los requerimientos formales se irán completando y refinando durante las siguientes etapas del TP.

| ID | Requerimiento | Tipo |
|---|---|---|
| RF01 | El sistema debe permitir buscar un lugar por nombre | Funcional |
| RF02 | El sistema debe permitir listar lugares según una categoría | Funcional |
| RF03 | El sistema debe mostrar el Top 10 de lugares mejor valorados | Funcional |
| RF04 | El sistema debe mostrar lugares relacionados con un lugar dado | Funcional |
| RF05 | El sistema debe sugerir lugares a partir de las preferencias, la cantidad de personas, las fechas y el presupuesto del grupo | Funcional |
| RNF01 | La búsqueda debe mantener un tiempo de respuesta aceptable con un volumen superior a 1.000 lugares | No funcional |

## 7. Fuera de alcance (por ahora)

- No se implementan autenticación ni perfiles de usuario.
- No se realizan reservas ni pagos.
- No se integran servicios externos de reservas.
- No se implementan recomendaciones mediante IA generativa.