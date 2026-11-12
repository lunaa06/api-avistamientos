from avistamientos.domain.entities import Avistamiento


class AvistamientoUseCases:
    """Coordina las acciones de la API sin depender de Flask ni de SQLite."""

    def __init__(self, repository, validator):
        self.repository = repository
        self.validator = validator

    def listar(self):
        return self.repository.listar()

    def obtener(self, identificador):
        return self.repository.obtener(identificador)

    def registrar(self, data):
        error = self.validator.validar(data)
        if error:
            raise ValueError(error)
        entidad = Avistamiento(
            especie=data["especie"].strip(),
            lugar=data["lugar"].strip(),
            fecha=data["fecha"],
            observador=data["observador"].strip(),
        )
        return self.repository.guardar(entidad)

    def actualizar(self, identificador, data):
        error = self.validator.validar(data)
        if error:
            raise ValueError(error)
        if self.repository.obtener(identificador) is None:
            return None
        entidad = Avistamiento(
            especie=data["especie"].strip(),
            lugar=data["lugar"].strip(),
            fecha=data["fecha"],
            observador=data["observador"].strip(),
            id=identificador,
        )
        return self.repository.actualizar(identificador, entidad)

    def eliminar(self, identificador):
        if self.repository.obtener(identificador) is None:
            return False
        self.repository.eliminar(identificador)
        return True

    def resumen(self):
        return self.repository.resumen()
