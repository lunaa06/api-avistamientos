
import sqlite3
import pytest
import app as modulo_app


@pytest.fixture
def cliente(monkeypatch):
    # Base de datos temporal compartida durante cada prueba.
    nombre_bd = "file:pruebas?mode=memory&cache=shared"

    conexion_principal = sqlite3.connect(nombre_bd, uri=True)
    conexion_principal.row_factory = sqlite3.Row

    def conectar_pruebas():
        conexion = sqlite3.connect(nombre_bd, uri=True)
        conexion.row_factory = sqlite3.Row
        return conexion

    # La API utilizará la base de datos temporal.
    monkeypatch.setattr(
        modulo_app,
        "conectar",
        conectar_pruebas
    )

    # Crear la tabla para las pruebas.
    conexion_principal.execute("""
        CREATE TABLE IF NOT EXISTS avistamientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            especie TEXT NOT NULL,
            lugar TEXT NOT NULL,
            fecha TEXT NOT NULL,
            observador TEXT NOT NULL
        )
    """)
    conexion_principal.commit()

    modulo_app.app.config["TESTING"] = True

    with modulo_app.app.test_client() as cliente_prueba:
        yield cliente_prueba

    conexion_principal.close()


def datos_validos():
    return {
        "especie": "Colibrí",
        "lugar": "Bogotá",
        "fecha": "2026-10-21",
        "observador": "Ana"
    }


def crear_registro(cliente):
    return cliente.post(
        "/avistamientos",
        json=datos_validos()
    )


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
    identificador = creado.json["id"]

    respuesta = cliente.get(f"/avistamientos/{identificador}")

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
    identificador = creado.json["id"]

    datos = datos_validos()
    datos["especie"] = "Tucán"

    respuesta = cliente.put(
        f"/avistamientos/{identificador}",
        json=datos
    )

    assert respuesta.status_code == 200
    assert respuesta.json["especie"] == "Tucán"


def test_actualizar_avistamiento_inexistente(cliente):
    respuesta = cliente.put(
        "/avistamientos/999",
        json=datos_validos()
    )

    assert respuesta.status_code == 404


def test_eliminar_avistamiento_correctamente(cliente):
    creado = crear_registro(cliente)
    identificador = creado.json["id"]

    respuesta = cliente.delete(f"/avistamientos/{identificador}")

    assert respuesta.status_code == 200

    consulta = cliente.get(f"/avistamientos/{identificador}")
    assert consulta.status_code == 404


def test_eliminar_avistamiento_inexistente(cliente):
    respuesta = cliente.delete("/avistamientos/999")

    assert respuesta.status_code == 404


def test_resumen_avistamientos(cliente):
    crear_registro(cliente)

    respuesta = cliente.get("/avistamientos/resumen")

    assert respuesta.status_code == 200
    assert respuesta.json == [
        {"especie": "Colibrí", "cantidad": 1}
    ]

def test_actualizar_avistamiento_con_especie_invalida(cliente):
    creado = crear_registro(cliente)
    identificador = creado.json["id"]

    datos = datos_validos()
    datos["especie"] = "AB"

    respuesta = cliente.put(
        f"/avistamientos/{identificador}",
        json=datos
    )

    assert respuesta.status_code == 400
    assert "especie" in respuesta.json["error"]
