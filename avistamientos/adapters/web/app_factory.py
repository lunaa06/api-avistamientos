from flask import Flask, jsonify, request

from avistamientos.application.use_cases.avistamientos import AvistamientoUseCases
from avistamientos.domain.validation import AvistamientoValidator
from avistamientos.infrastructure.persistence.sqlite_repository import (
    SQLiteAvistamientoRepository,
)


def create_app(repository=None, validator=None):
    """Construye Flask y conecta los adaptadores con los casos de uso."""
    app = Flask(__name__)
    repository = repository or SQLiteAvistamientoRepository()
    validator = validator or AvistamientoValidator()
    use_cases = AvistamientoUseCases(repository, validator)

    @app.get("/")
    def inicio():
        return jsonify({"mensaje": "API de avistamientos funcionando"}), 200

    @app.get("/avistamientos")
    def listar_avistamientos():
        return jsonify(use_cases.listar()), 200

    @app.get("/avistamientos/<int:identificador>")
    def obtener_avistamiento(identificador):
        resultado = use_cases.obtener(identificador)
        if resultado is None:
            return jsonify({"error": "Avistamiento no encontrado"}), 404
        return jsonify(resultado), 200

    @app.post("/avistamientos")
    def crear_avistamiento():
        datos = request.get_json(silent=True)
        try:
            resultado = use_cases.registrar(datos)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        return jsonify(resultado), 201

    @app.put("/avistamientos/<int:identificador>")
    def actualizar_avistamiento(identificador):
        datos = request.get_json(silent=True)
        try:
            resultado = use_cases.actualizar(identificador, datos)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        if resultado is None:
            return jsonify({"error": "Avistamiento no encontrado"}), 404
        return jsonify(resultado), 200

    @app.delete("/avistamientos/<int:identificador>")
    def eliminar_avistamiento(identificador):
        if not use_cases.eliminar(identificador):
            return jsonify({"error": "Avistamiento no encontrado"}), 404
        return jsonify({"mensaje": "Avistamiento eliminado correctamente"}), 200

    @app.get("/avistamientos/resumen")
    def resumen_avistamientos():
        return jsonify(use_cases.resumen()), 200

    app.extensions["avistamiento_repository"] = repository
    app.extensions["avistamiento_use_cases"] = use_cases
    return app
