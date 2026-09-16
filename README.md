# ¿Dónde vamos?

Proyecto integrador de **Estructura de Datos**, desarrollado en Python.

## Descripción

¿Dónde vamos? es un sistema que ayuda a parejas o grupos pequeños de amigos a encontrar y organizar una salida considerando sus preferencias y presupuesto. Su v1 permite buscar, listar y filtrar 50 lugares reales de CABA (parrillas, cafeterías, bares, heladerías, etc.) considerando puntuación (0–5), costo (1–3) y horarios de apertura/cierre; además permite ver los participantes de cada salida.

## Ejecución

```bash
python main.py
```

## Pruebas

```bash
python -m unittest discover tests
```

## Demo

![Demo de la v1](docs/capturas/tp1-demo.png)

## Estructura del repositorio

```text
proyecto/
├── main.py
├── README.md
├── .gitignore
├── docs/
│   ├── 01-requerimientos.md
│   ├── 02-casos-de-uso.md
│   ├── 03-diagrama-clases.md
│   ├── 04-diagrama-datos.md
│   ├── 05-gestion-proyecto.md
│   └── capturas/
├── modelos/
│   ├── lugar.py
│   └── salida.py
├── servicios/
│   └── catalogo.py
├── ui/
│   └── terminal.py
├── datos/
│   ├── lugares.json
│   ├── lugares-antiguo.json
│   └── salidas.json
├── estructuras/      ← próximos TPs (TP3+)
├── algoritmos/       ← próximos TPs (TP3+)
└── tests/
    └── test_catalogo.py
```

En TP0 se documentó la propuesta y se preparó el repositorio. En TP1 se implementó la v1: modelo de dominio, catálogo, terminal y pruebas.