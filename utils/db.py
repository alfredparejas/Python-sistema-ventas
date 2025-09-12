import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        return mysql.connector.connect(
            host='172.31.176.1',   # IP Windows desde WSL2
            user='app_user',
            password='App1234!',
            database='sistemaventas',
            port=3306
        )
    except Error as ex:
        print("Error al conectar a la base de datos:", ex)
        return None
