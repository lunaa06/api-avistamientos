import pytest

from avistamientos.adapters.web.app_factory import create_app
from avistamientos.infrastructure.persistence.sqlite_repository import SQLiteAvistamientoRepository


@pytest.fixture
def cliente():
    repositorio = SQLiteAvistamientoRepository(":memory:")
    app = create_app(repository=repositorio)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
    repositorio.close()


def datos_validos():
    return {"especie": "Colibrí", "lugar": "Bogotá", "fecha": "2026-10-21", "observador": "Ana"}


def crear_registro(cliente):
    return cliente.post("/avistamientos", json=datos_validos())


def test_inicio_responde_correctamente(cliente):
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json["mensaje"] == "API de avistamientos funcionando"


def test_listar_avistamientos(cliente):
    crear_registro(cliente)
    respuesta = cliente.get("/avistamientos")
    assert respuesta.status_code == 200
    assert len(respuesta.json) == 1


def test_obtener_avistamiento_existente(cliente):
    creado = crear_registro(cliente)
    respuesta = cliente.get(f"/avistamientos/{creado.json['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json["especie"] == "Colibrí"


def test_obtener_avistamiento_inexistente(cliente):
    respuesta = cliente.get("/avistamientos/999")
    assert respuesta.status_code == 404
    assert respuesta.json["error"] == "Avistamiento no encontrado"


def test_crear_avistamiento_correctamente(cliente):
    respuesta = crear_registro(cliente)
    assert respuesta.status_code == 201
    assert respuesta.json["especie"] == "Colibrí"
    assert "id" in respuesta.json


def test_crear_avistamiento_con_especie_invalida(cliente):
    datos = datos_validos()
    datos["especie"] = "AB"
    respuesta = cliente.post("/avistamientos", json=datos)
    assert respuesta.status_code == 400
    assert "especie" in respuesta.json["error"]


def test_actualizar_avistamiento_correctamente(cliente):
    creado = crear_registro(cliente)
    datos = datos_validos()
    datos["especie"] = "Tucán"
    respuesta = cliente.put(f"/avistamientos/{creado.json['id']}", json=datos)
    assert respuesta.status_code == 200
    assert respuesta.json["especie"] == "Tucán"


def test_actualizar_avistamiento_inexistente(cliente):
    respuesta = cliente.put("/avistamientos/999", json=datos_validos())
    assert respuesta.status_code == 404


def test_eliminar_avistamiento_correctamente(cliente):
    creado = crear_registro(cliente)
    identificador = creado.json["id"]
    respuesta = cliente.delete(f"/avistamientos/{identificador}")
    assert respuesta.status_code == 200
    assert cliente.get(f"/avistamientos/{identificador}").status_code == 404


def test_eliminar_avistamiento_inexistente(cliente):
    respuesta = cliente.delete("/avistamientos/999")
    assert respuesta.status_code == 404


def test_resumen_avistamientos(cliente):
    crear_registro(cliente)
    respuesta = cliente.get("/avistamientos/resumen")
    assert respuesta.status_code == 200
    assert respuesta.json == [{"especie": "Colibrí", "cantidad": 1}]


def test_actualizar_avistamiento_con_especie_invalida(cliente):
    creado = crear_registro(cliente)
    datos = datos_validos()
    datos["especie"] = "AB"
    respuesta = cliente.put(f"/avistamientos/{creado.json['id']}", json=datos)
    assert respuesta.status_code == 400
    assert "especie" in respuesta.json["error"]
