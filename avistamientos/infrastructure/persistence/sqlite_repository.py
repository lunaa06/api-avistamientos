import sqlite3


class SQLiteAvistamientoRepository:
    """Implementación del repositorio usando SQLite."""

    def __init__(self, database_path="avistamientos.db"):
        self.database_path = database_path
        self._connection = sqlite3.connect(database_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS avistamientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                especie TEXT NOT NULL,
                lugar TEXT NOT NULL,
                fecha TEXT NOT NULL,
                observador TEXT NOT NULL
            )
        """)
        self._connection.commit()

    @staticmethod
    def _as_dict(row):
        return dict(row) if row is not None else None

    def listar(self):
        rows = self._connection.execute(
            "SELECT * FROM avistamientos ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]

    def obtener(self, identificador):
        row = self._connection.execute(
            "SELECT * FROM avistamientos WHERE id = ?", (identificador,)
        ).fetchone()
        return self._as_dict(row)

    def guardar(self, datos):
        cursor = self._connection.execute(
            """INSERT INTO avistamientos (especie, lugar, fecha, observador)
               VALUES (?, ?, ?, ?)""",
            (datos["especie"], datos["lugar"], datos["fecha"], datos["observador"]),
        )
        self._connection.commit()
        return self.obtener(cursor.lastrowid)

    def actualizar(self, identificador, datos):
        self._connection.execute(
            """UPDATE avistamientos
               SET especie = ?, lugar = ?, fecha = ?, observador = ?
               WHERE id = ?""",
            (datos["especie"], datos["lugar"], datos["fecha"],
             datos["observador"], identificador),
        )
        self._connection.commit()
        return self.obtener(identificador)

    def eliminar(self, identificador):
        self._connection.execute(
            "DELETE FROM avistamientos WHERE id = ?", (identificador,)
        )
        self._connection.commit()

    def resumen(self):
        rows = self._connection.execute(
            """SELECT especie, COUNT(*) AS cantidad
               FROM avistamientos GROUP BY especie ORDER BY especie"""
        ).fetchall()
        return [dict(row) for row in rows]

    def close(self):
        self._connection.close()
