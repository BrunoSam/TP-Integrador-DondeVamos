# Gestión del proyecto

- **Tablero:** https://trello.com/b/s3XjcekO/tp-integrador-estructuras-de-datos-donde-vamos
- **Metodología:** Scrum simplificado — un sprint por TP.
- **Columnas:** Backlog · En progreso · En revisión · Hecho.

## Sprint TP0 (Lanzamiento)

- [x] Definir dominio y justificarlo
- [x] Definir problema y usuario objetivo
- [x] Escribir propuesta inicial
- [x] Definir 5 funcionalidades
- [x] Bocetar diagrama de clases inicial
- [x] Armar estructura del repositorio y README
- [ ] Crear tablero y cargar las 5 funcionalidades como tarjetas
- [ ] Enviar nómina del grupo al docente
- [ ] Realizar primer commit

### Retro TP0

Se definió un problema concreto, un usuario objetivo y un alcance inicial acotado. El modelo y los requerimientos podrán refinarse durante las siguientes etapas a partir de la implementación y de las estructuras de datos de la cursada.

## Sprint TP1 (Objetos y clases — v1)

- [x] Modelar la clase `Lugar` con encapsulamiento (@property y `__repr__`)
- [x] Implementar `Catalogo` con carga desde JSON, buscar, listar y filtrar
- [x] Armar dataset `datos/lugares.json` (50 lugares, 12 de zona sur GBA)
- [x] Implementar terminal con menú, bucle y manejo de opción inválida
- [x] Crear `main.py` como punto de entrada
- [x] Escribir pruebas unitarias que corren
- [x] Actualizar documentación (diagrama, casos de uso, README)
- [x] Sacar captura de la demo en `docs/capturas/`
- [ ] Realizar commit/PR de la v1

### Retro TP1

Se implementó la v1 completa: clase `Lugar` con encapsulamiento (@property, `__repr__`), catálogo con búsqueda por nombre exacta y parcial sin distinguir mayúsculas, y terminal desacoplada de la lógica (testeable sin UI). El dataset quedó con 50 lugares reales de CABA (parrillas, cafeterías, bares, heladerías, pizzerías y bodegones), cada uno con puntuación (0–5), costo (1–3) y horarios de apertura/cierre.

Qué mejorar: ir sumando más datos reales a medida que crece el catálogo y arrancar el hábito de commits por unidad de trabajo (la historia del repo se evalúa).
