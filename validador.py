
import re
from datetime import date, datetime


class Reloj:
    """Obtiene la fecha actual del sistema."""

    def hoy(self):
        return date.today()


class ValidadorDeAvistamiento:
    """Valida los datos de un avistamiento."""

    def __init__(self, reloj=None):
        self.reloj = reloj if reloj is not None else Reloj()

    def validar(self, datos):
        if not isinstance(datos, dict):
            return "El cuerpo debe ser un JSON válido"

        especie = datos.get("especie")
        if not isinstance(especie, str) or not 3 <= len(especie.strip()) <= 50:
            return "El campo especie debe tener entre 3 y 50 caracteres"

        fecha = datos.get("fecha")
        if not isinstance(fecha, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
            return "El campo fecha debe tener el formato AAAA-MM-DD"

        try:
            fecha_avistamiento = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return "El campo fecha no es una fecha válida"

        if fecha_avistamiento > self.reloj.hoy():
            return "El campo fecha no puede ser posterior a hoy"

        lugar = datos.get("lugar")
        if not isinstance(lugar, str) or not lugar.strip():
            return "El campo lugar no puede estar vacío"

        observador = datos.get("observador")
        if not isinstance(observador, str) or not observador.strip():
            return "El campo observador no puede estar vacío"

        return None
