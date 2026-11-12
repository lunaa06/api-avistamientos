from flask import Blueprint, request


def crear_blueprint(casos_de_uso):
    rutas = Blueprint("avistamientos", __name__)

    @rutas.get("/")
    def inicio():
        return {"mensaje": "API de avistamientos funcionando"}, 200

    @rutas.get("/avistamientos")
    def listar():
        return casos_de_uso.listar(), 200

    @rutas.get("/avistamientos/<int:identificador>")
    def obtener(identificador):
        resultado = casos_de_uso.obtener(identificador)
        if resultado is None:
            return {"error": "Avistamiento no encontrado"}, 404
        return resultado, 200

    @rutas.post("/avistamientos")
    def registrar():
        datos = request.get_json(silent=True)
        try:
            resultado = casos_de_uso.registrar(datos)
        except ValueError as error:
            return {"error": str(error)}, 400
        return resultado, 201

    @rutas.put("/avistamientos/<int:identificador>")
    def actualizar(identificador):
        datos = request.get_json(silent=True)
        try:
            resultado = casos_de_uso.actualizar(identificador, datos)
        except ValueError as error:
            return {"error": str(error)}, 400
        if resultado is None:
            return {"error": "Avistamiento no encontrado"}, 404
        return resultado, 200

    @rutas.delete("/avistamientos/<int:identificador>")
    def eliminar(identificador):
        if not casos_de_uso.eliminar(identificador):
            return {"error": "Avistamiento no encontrado"}, 404
        return {"mensaje": "Avistamiento eliminado correctamente"}, 200

    @rutas.get("/avistamientos/resumen")
    def resumen():
        return casos_de_uso.resumen(), 200

    return rutas
