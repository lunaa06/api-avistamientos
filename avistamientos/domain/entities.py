from dataclasses import dataclass


@dataclass(frozen=True)
class Avistamiento:
    """Entidad principal del dominio."""

    especie: str
    lugar: str
    fecha: str
    observador: str
    id: int | None = None

    def to_dict(self):
        return {
            "id": self.id,
            "especie": self.especie,
            "lugar": self.lugar,
            "fecha": self.fecha,
            "observador": self.observador,
        }
