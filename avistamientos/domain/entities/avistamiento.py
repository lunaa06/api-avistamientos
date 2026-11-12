from dataclasses import dataclass


@dataclass
class Avistamiento:
    """Representa un avistamiento sin depender de Flask ni de SQLite."""

    especie: str
    lugar: str
    fecha: str
    observador: str
    id: int | None = None

    def como_dict(self):
        return {
            "id": self.id,
            "especie": self.especie,
            "lugar": self.lugar,
            "fecha": self.fecha,
            "observador": self.observador,
        }
