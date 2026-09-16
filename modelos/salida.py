class Salida:
    """Representa una salida armada por el grupo: nombre y lista de participantes."""

    def __init__(self, id, nombre, participantes):
        self._id = id
        self._nombre = nombre
        self._participantes = participantes

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def participantes(self) -> list:
        return self._participantes

    def __repr__(self) -> str:
        return f"{self._nombre} ({len(self._participantes)} participantes)"