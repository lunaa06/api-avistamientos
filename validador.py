"""Compatibilidad con las pruebas anteriores.

La implementación oficial del validador ahora vive en la capa de dominio.
"""
from avistamientos.domain.services.validador import Reloj, ValidadorDeAvistamiento

__all__ = ["Reloj", "ValidadorDeAvistamiento"]
