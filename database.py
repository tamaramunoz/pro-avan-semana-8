import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            # establecemos la conexión con la base de datos
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            return True, None
        except Error as e:
            return False, str(e)

    def obtener_agencias(self):
        query = "SELECT ID, Nombre, Pais, FechaCreacion FROM AgenciaEspacial"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def obtener_agencia_por_id(self, agencia_id):
        query = "SELECT ID, Nombre, Pais, FechaCreacion FROM AgenciaEspacial WHERE ID = %s"
        self.cursor.execute(query, (agencia_id,))
        return self.cursor.fetchone()

    def agregar_agencia(self, agencia_id, nombre, pais, fecha):
        query = "INSERT INTO AgenciaEspacial (ID, Nombre, Pais, FechaCreacion) VALUES (%s, %s, %s, %s)"
        values = (agencia_id, nombre, pais, fecha)
        self.cursor.execute(query, values)
        self.connection.commit()

    def actualizar_agencia(self, agencia_id, nombre, pais, fecha):
        query = "UPDATE AgenciaEspacial SET Nombre = %s, Pais = %s, FechaCreacion = %s WHERE ID = %s"
        values = (nombre, pais, fecha, agencia_id)
        self.cursor.execute(query, values)
        self.connection.commit()

    def borrar_agencia(self, agencia_id):
        query = "DELETE FROM AgenciaEspacial WHERE ID = %s"
        self.cursor.execute(query, (agencia_id,))
        self.connection.commit()

    # cerramos el cursor y la conexión activas
    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

