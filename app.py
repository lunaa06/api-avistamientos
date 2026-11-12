from flask import Flask

from database import conectar, crear_tabla
from avistamientos.adapters.web.routes import crear_blueprint
from avistamientos.application.use_cases.avistamientos import AvistamientoUseCases
from avistamientos.domain.services.validador import ValidadorDeAvistamiento
from avistamientos.infrastructure.persistence.sqlite_avistamiento_repository import (
    SQLiteAvistamientoRepository,
)


def crear_app():
    """Construye Flask y conecta los adaptadores con los casos de uso."""
    aplicacion = Flask(__name__)
    repositorio = SQLiteAvistamientoRepository(lambda: conectar())
    validador = ValidadorDeAvistamiento()
    casos_de_uso = AvistamientoUseCases(repositorio, validador)
    aplicacion.register_blueprint(crear_blueprint(casos_de_uso))
    return aplicacion


app = crear_app()

if __name__ == "__main__":
    crear_tabla()
    app.run(debug=True)
