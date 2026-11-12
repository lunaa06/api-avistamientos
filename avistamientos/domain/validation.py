import re
from datetime import date, datetime


class SystemClock:
    """Proporciona la fecha actual del sistema."""

    def today(self):
        return date.today()


class AvistamientoValidator:
    """Contiene las reglas de validación propias del dominio."""

    def __init__(self, clock=None):
        self.clock = clock or SystemClock()

    def validate(self, data):
        if not isinstance(data, dict):
            return "El cuerpo debe ser un JSON válido"

        especie = data.get("especie")
        if not isinstance(especie, str) or not 3 <= len(especie.strip()) <= 50:
            return "El campo especie debe tener entre 3 y 50 caracteres"

        fecha = data.get("fecha")
        if not isinstance(fecha, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
            return "El campo fecha debe tener el formato AAAA-MM-DD"

        try:
            fecha_avistamiento = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return "El campo fecha no es una fecha válida"

        if fecha_avistamiento > self.clock.today():
            return "El campo fecha no puede ser posterior a hoy"

        lugar = data.get("lugar")
        if not isinstance(lugar, str) or not lugar.strip():
            return "El campo lugar no puede estar vacío"

        observador = data.get("observador")
        if not isinstance(observador, str) or not observador.strip():
            return "El campo observador no puede estar vacío"

        return None
