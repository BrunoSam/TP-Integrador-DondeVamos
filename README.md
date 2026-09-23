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

## Experimentos (TP2)

```bash
python datos/generar.py                       # datasets sintéticos (100 a 100.000)
python algoritmos/experimentos/medicion.py    # mide secuencial vs binaria
```

Informe y análisis: [`docs/tp2-experimentos.md`](docs/tp2-experimentos.md).

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
│   ├── salidas.json
│   └── generar.py        ← TP2 (datasets sintéticos para experimentos)
├── algoritmos/
│   └── experimentos/     ← TP2 (medicion.py, grafico.py)
├── estructuras/          ← próximos TPs (TP3+)
├── algoritmos/           ← próximos TPs (TP3+)
└── tests/
    └── test_catalogo.py
```

En TP0 se documentó la propuesta y se preparó el repositorio. En TP1 se implementó la v1: modelo de dominio, catálogo, terminal y pruebas. En TP2 se analizó la complejidad de la búsqueda por nombre: se comparó la búsqueda secuencial (O(n)) con una búsqueda binaria sobre lista ordenada (O(log n)), midiendo con datasets de 100 a 100.000 lugares (`docs/tp2-experimentos.md`).