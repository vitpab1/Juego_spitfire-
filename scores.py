import sqlite3



def insert_score(score, name):
    with sqlite3.connect("scores.db") as conexion:
        try:
            sentencia = '''CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                score REAL
            )'''
            conexion.execute(sentencia)
            print("Se creó la tabla jugadores")
        except sqlite3.OperationalError:
            print("La tabla jugadores ya existe")

        personaje = (name, score)

        try:
            conexion.execute("INSERT INTO jugadores (nombre, score) VALUES (?, ?)", personaje)
            conexion.commit()
            print("Se insertó el personaje en la tabla")
        except sqlite3.Error as error:
            print("Error al insertar el personaje:", error)

