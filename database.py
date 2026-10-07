import sqlite3


DATABASE = "avistamientos.db"


def conectar():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS avistamientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            especie TEXT NOT NULL,
            lugar TEXT NOT NULL,
            fecha TEXT NOT NULL,
            observador TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()