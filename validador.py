from avistamientos.domain.validation import AvistamientoValidator


class _ClockAdapter:
    """Adapta el reloj usado en los talleres anteriores al contrato actual."""

    def __init__(self, legacy_clock):
        self.legacy_clock = legacy_clock

    def today(self):
        return self.legacy_clock.hoy()


class ValidadorDeAvistamiento:
    """Compatibilidad con las pruebas y el código del taller anterior."""

    def __init__(self, reloj=None):
        clock = _ClockAdapter(reloj) if reloj is not None else None
        self._validator = AvistamientoValidator(clock)

    def validar(self, datos):
        return self._validator.validate(datos)
