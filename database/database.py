import mysql.connector

class DatabaseManager:
    def __init__(self):
        self._db = mysql.connector.connect(
            host = "sql12.freesqldatabase.com",
            user = "sql12666408",
            password = "LyqraRUgFf",
            database = "sql12666408",
            )

    def get_my_db(self):
        return self._db
    
    def get_connection(self):
        # Add your connection details here
        return mysql.connector.connect(user="sql12666408", password="LyqraRUgFf", host="sql12.freesqldatabase.com", database="sql12666408")
