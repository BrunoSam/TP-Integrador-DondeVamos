class Lugar:
    """Representa un lugar o actividad posible para una salida (café, restaurante, bar, parrilla, etc.)."""

    def __init__(self, id, nombre, zona, categoria, puntuacion, horario_apertura, horario_cierre, costo):
        self._id = id
        self._nombre = nombre
        self._zona = zona
        self._categoria = categoria
        self._puntuacion = puntuacion
        self._horario_apertura = horario_apertura
        self._horario_cierre = horario_cierre
        self._costo = costo

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def zona(self) -> str:
        return self._zona

    @property
    def categoria(self) -> str:
        return self._categoria

    @property
    def puntuacion(self) -> float:
        return self._puntuacion

    @property
    def horario_apertura(self) -> str:
        return self._horario_apertura

    @property
    def horario_cierre(self) -> str:
        return self._horario_cierre

    @property
    def costo(self) -> int:
        return self._costo

    def __repr__(self) -> str:
        return (
            f"{self._nombre} — {self._categoria} ({self._zona}) "
            f"[⭐ {self._puntuacion} | {'$' * self._costo} | {self._horario_apertura}-{self._horario_cierre}]"
        )