from avistamientos.domain.entities import Avistamiento


class AvistamientoUseCases:
    """Coordina las operaciones de la API sin conocer Flask ni SQLite."""

    def __init__(self, repository, validator):
        self.repository = repository
        self.validator = validator

    def listar(self):
        return self.repository.listar()

    def obtener(self, identificador):
        return self.repository.obtener(identificador)

    def registrar(self, data):
        error = self.validator.validate(data)
        if error:
            raise ValueError(error)
        return self.repository.guardar(self._normalizar(data))

    def actualizar(self, identificador, data):
        error = self.validator.validate(data)
        if error:
            raise ValueError(error)
        if self.repository.obtener(identificador) is None:
            return None
        return self.repository.actualizar(identificador, self._normalizar(data))

    def eliminar(self, identificador):
        if self.repository.obtener(identificador) is None:
            return False
        self.repository.eliminar(identificador)
        return True

    def resumen(self):
        return self.repository.resumen()

    @staticmethod
    def _normalizar(data):
        return {
            "especie": data["especie"].strip(),
            "lugar": data["lugar"].strip(),
            "fecha": data["fecha"],
            "observador": data["observador"].strip(),
        }
