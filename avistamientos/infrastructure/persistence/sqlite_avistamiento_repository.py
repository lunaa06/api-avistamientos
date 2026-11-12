class SQLiteAvistamientoRepository:
    """Implementación del repositorio usando SQLite."""

    def __init__(self, conectar):
        self.conectar = conectar

    @staticmethod
    def _fila(fila):
        return dict(fila) if fila is not None else None

    def listar(self):
        conexion = self.conectar()
        filas = conexion.execute("SELECT * FROM avistamientos").fetchall()
        conexion.close()
        return [dict(fila) for fila in filas]

    def obtener(self, identificador):
        conexion = self.conectar()
        fila = conexion.execute(
            "SELECT * FROM avistamientos WHERE id = ?", (identificador,)
        ).fetchone()
        conexion.close()
        return self._fila(fila)

    def guardar(self, avistamiento):
        datos = avistamiento.como_dict()
        conexion = self.conectar()
        cursor = conexion.execute(
            """INSERT INTO avistamientos (especie, lugar, fecha, observador)
               VALUES (?, ?, ?, ?)""",
            (datos["especie"], datos["lugar"], datos["fecha"], datos["observador"]),
        )
        conexion.commit()
        identificador = cursor.lastrowid
        fila = conexion.execute(
            "SELECT * FROM avistamientos WHERE id = ?", (identificador,)
        ).fetchone()
        conexion.close()
        return self._fila(fila)

    def actualizar(self, identificador, avistamiento):
        datos = avistamiento.como_dict()
        conexion = self.conectar()
        conexion.execute(
            """UPDATE avistamientos
               SET especie = ?, lugar = ?, fecha = ?, observador = ?
               WHERE id = ?""",
            (datos["especie"], datos["lugar"], datos["fecha"], datos["observador"], identificador),
        )
        conexion.commit()
        fila = conexion.execute(
            "SELECT * FROM avistamientos WHERE id = ?", (identificador,)
        ).fetchone()
        conexion.close()
        return self._fila(fila)

    def eliminar(self, identificador):
        conexion = self.conectar()
        cursor = conexion.execute(
            "DELETE FROM avistamientos WHERE id = ?", (identificador,)
        )
        conexion.commit()
        eliminado = cursor.rowcount > 0
        conexion.close()
        return eliminado

    def resumen(self):
        conexion = self.conectar()
        filas = conexion.execute(
            """SELECT especie, COUNT(*) AS cantidad
               FROM avistamientos GROUP BY especie"""
        ).fetchall()
        conexion.close()
        return [dict(fila) for fila in filas]
