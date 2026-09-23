"""Genera datasets sintéticos para los experimentos del TP2.

Uso:  python datos/generar.py
Genera datos/lugares_{n}.json con el mismo esquema que datos/lugares.json.
"""

import json
import random

ZONAS = [
    "Almagro", "Belgrano", "Chacarita", "Colegiales", "Palermo",
    "Palermo Soho", "Puerto Madero", "Recoleta", "San Telmo", "Villa Crespo",
]
CATEGORIAS = [
    "bar", "bodegon", "cafeteria", "heladeria", "parrilla",
    "pizzeria", "restaurante",
]


def generar(n: int, ruta: str) -> None:
    lugares = [
        {
            "id": i,
            "nombre": f"Lugar {i}",
            "zona": random.choice(ZONAS),
            "categoria": random.choice(CATEGORIAS),
            "puntuacion": round(random.uniform(1.0, 5.0), 1),
            "horario_apertura": f"{random.randint(8, 12):02d}:00",
            "horario_cierre": f"{random.randint(0, 23):02d}:00",
            "costo": random.randint(1, 3),
        }
        for i in range(n)
    ]
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(lugares, archivo, ensure_ascii=False, indent=2)
    print(ruta)


def main() -> None:
    tamaños = (100, 1_000, 10_000, 100_000)
    for n in tamaños:
        generar(n, rf"datos/lugares_{n}.json")


if __name__ == "__main__":
    main()