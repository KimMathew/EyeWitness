import mysql.connector

class DatabaseManager:
    def __init__(self):
        self._db = mysql.connector.connect(
            host = "sql12.freesqldatabase.com",
            user = "sql12662532",
            password = "viDRIhzYSq",
            database = "sql12662532",
            )

    def get_my_db(self):
        return self._db
    
