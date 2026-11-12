from datetime import date

from avistamientos.application.use_cases.avistamientos import AvistamientoUseCases
from avistamientos.domain.validation import AvistamientoValidator


class RelojFijo:
    def today(self):
        return date(2026, 10, 21)


class RepositorioEnMemoria:
    def __init__(self):
        self.items = {}
        self.next_id = 1

    def listar(self):
        return list(self.items.values())

    def obtener(self, identificador):
        return self.items.get(identificador)

    def guardar(self, datos):
        item = {"id": self.next_id, **datos}
        self.items[self.next_id] = item
        self.next_id += 1
        return item

    def actualizar(self, identificador, datos):
        self.items[identificador] = {"id": identificador, **datos}
        return self.items[identificador]

    def eliminar(self, identificador):
        self.items.pop(identificador, None)

    def resumen(self):
        conteo = {}
        for item in self.items.values():
            especie = item["especie"]
            conteo[especie] = conteo.get(especie, 0) + 1
        return [{"especie": especie, "cantidad": cantidad} for especie, cantidad in sorted(conteo.items())]


def datos_validos():
    return {"especie": "Colibrí", "lugar": "Bogotá", "fecha": "2026-10-21", "observador": "Ana"}


def crear_casos_de_uso():
    return AvistamientoUseCases(RepositorioEnMemoria(), AvistamientoValidator(RelojFijo()))


def test_registrar_y_consultar_avistamiento():
    casos = crear_casos_de_uso()
    creado = casos.registrar(datos_validos())
    assert creado["id"] == 1
    assert casos.obtener(1)["especie"] == "Colibrí"


def test_no_registra_datos_invalidos():
    casos = crear_casos_de_uso()
    datos = datos_validos()
    datos["especie"] = "AB"
    try:
        casos.registrar(datos)
        assert False, "Se esperaba un error de validación"
    except ValueError as error:
        assert "especie" in str(error)


def test_actualizar_y_eliminar():
    casos = crear_casos_de_uso()
    casos.registrar(datos_validos())
    datos = datos_validos()
    datos["especie"] = "Tucán"
    assert casos.actualizar(1, datos)["especie"] == "Tucán"
    assert casos.eliminar(1) is True
    assert casos.obtener(1) is None


def test_operaciones_sobre_identificador_inexistente():
    casos = crear_casos_de_uso()
    assert casos.actualizar(99, datos_validos()) is None
    assert casos.eliminar(99) is False
