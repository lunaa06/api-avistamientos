from flask import Flask, request
from database import conectar, crear_tabla

app = Flask(__name__)


@app.route("/")
def inicio():
    return {"mensaje": "API de avistamientos funcionando"}


@app.route("/avistamientos", methods=["GET"])
def listar_avistamientos():
    conexion = conectar()

    avistamientos = conexion.execute(
        "SELECT * FROM avistamientos"
    ).fetchall()

    conexion.close()

    resultado = [dict(avistamiento) for avistamiento in avistamientos]

    return resultado, 200


@app.route("/avistamientos/<int:id>", methods=["GET"])
def obtener_avistamiento(id):
    conexion = conectar()

    avistamiento = conexion.execute(
        "SELECT * FROM avistamientos WHERE id = ?",
        (id,)
    ).fetchone()

    conexion.close()

    if avistamiento is None:
        return {"error": "Avistamiento no encontrado"}, 404

    return dict(avistamiento), 200


@app.route("/avistamientos/<int:id>", methods=["PUT"])
def actualizar_avistamiento(id):
    datos = request.get_json(silent=True)

    if datos is None:
        return {"error": "No se recibió un JSON válido"}, 400

    campos = ["especie", "lugar", "fecha", "observador"]

    for campo in campos:
        if campo not in datos or not datos[campo]:
            return {"error": f"Falta el campo: {campo}"}, 400

    conexion = conectar()

    avistamiento = conexion.execute(
        "SELECT * FROM avistamientos WHERE id = ?",
        (id,)
    ).fetchone()

    if avistamiento is None:
        conexion.close()
        return {"error": "Avistamiento no encontrado"}, 404

    conexion.execute(
        """
        UPDATE avistamientos
        SET especie = ?, lugar = ?, fecha = ?, observador = ?
        WHERE id = ?
        """,
        (
            datos["especie"],
            datos["lugar"],
            datos["fecha"],
            datos["observador"],
            id
        )
    )

    conexion.commit()

    actualizado = conexion.execute(
        "SELECT * FROM avistamientos WHERE id = ?",
        (id,)
    ).fetchone()

    conexion.close()

    return dict(actualizado), 200
@app.route("/avistamientos/<int:id>", methods=["DELETE"])
def eliminar_avistamiento(id):
    conexion = conectar()

    avistamiento = conexion.execute(
        "SELECT * FROM avistamientos WHERE id = ?",
        (id,)
    ).fetchone()

    if avistamiento is None:
        conexion.close()
        return {"error": "Avistamiento no encontrado"}, 404

    conexion.execute(
        "DELETE FROM avistamientos WHERE id = ?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Avistamiento eliminado correctamente"}, 200

@app.route("/avistamientos", methods=["POST"])
def crear_avistamiento():
    datos = request.get_json(silent=True)

    print("DATOS RECIBIDOS:", datos)

    if datos is None:
        return {"error": "No se recibió un JSON válido"}, 400

    campos = ["especie", "lugar", "fecha", "observador"]

    for campo in campos:
        if campo not in datos or not datos[campo]:
            return {"error": f"Falta el campo: {campo}"}, 400

    conexion = conectar()

    cursor = conexion.execute(
        """
        INSERT INTO avistamientos (especie, lugar, fecha, observador)
        VALUES (?, ?, ?, ?)
        """,
        (
            datos["especie"],
            datos["lugar"],
            datos["fecha"],
            datos["observador"]
        )
    )

    conexion.commit()

    id_nuevo = cursor.lastrowid

    avistamiento = conexion.execute(
        "SELECT * FROM avistamientos WHERE id = ?",
        (id_nuevo,)
    ).fetchone()

    conexion.close()

    return dict(avistamiento), 201
@app.route("/avistamientos/resumen", methods=["GET"])
def resumen_avistamientos():
    conexion = conectar()

    resumen = conexion.execute(
        """
        SELECT especie, COUNT(*) AS cantidad
        FROM avistamientos
        GROUP BY especie
        """
    ).fetchall()

    conexion.close()

    resultado = [dict(item) for item in resumen]

    return resultado, 200

if __name__ == "__main__":
    crear_tabla()
    app.run(debug=True)