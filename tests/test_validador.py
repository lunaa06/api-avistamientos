
from datetime import date
from validador import ValidadorDeAvistamiento


class RelojFijo:
    """Doble de prueba que devuelve una fecha controlada."""

    def hoy(self):
        return date(2026, 10, 21)


def datos_validos():
    return {
        "especie": "Colibrí",
        "fecha": "2026-10-21",
        "lugar": "Bogotá",
        "observador": "Ana"
    }


def test_datos_validos_se_aceptan():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is None


def test_especie_de_dos_caracteres_se_rechaza():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()
    datos["especie"] = "AB"

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is not None
    assert "especie" in resultado


def test_especie_de_tres_caracteres_se_acepta():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()
    datos["especie"] = "Ave"

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is None


def test_especie_de_cincuenta_caracteres_se_acepta():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()
    datos["especie"] = "A" * 50

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is None


def test_especie_de_cincuenta_y_un_caracteres_se_rechaza():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()
    datos["especie"] = "A" * 51

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is not None
    assert "especie" in resultado


def test_fecha_de_hoy_se_acepta():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is None


def test_fecha_de_manana_se_rechaza():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()
    datos["fecha"] = "2026-10-22"

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is not None
    assert "posterior a hoy" in resultado


def test_formato_de_fecha_incorrecto_se_rechaza():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()
    datos["fecha"] = "21/10/2026"

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is not None
    assert "fecha" in resultado


def test_fecha_inexistente_se_rechaza():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()
    datos["fecha"] = "2026-02-30"

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is not None


def test_lugar_vacio_se_rechaza():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()
    datos["lugar"] = "   "

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is not None
    assert "lugar" in resultado


def test_observador_vacio_se_rechaza():
    # Arrange
    validador = ValidadorDeAvistamiento(RelojFijo())
    datos = datos_validos()
    datos["observador"] = ""

    # Act
    resultado = validador.validar(datos)

    # Assert
    assert resultado is not None
    assert "observador" in resultado

def test_datos_que_no_son_diccionario_se_rechazan():
    validador = ValidadorDeAvistamiento()

    # Arrange: preparar datos que no son un diccionario.
    datos = None

    # Act: ejecutar la validación.
    resultado = validador.validar(datos)

    # Assert: comprobar que se rechazan.
    assert resultado == "El cuerpo debe ser un JSON válido"
