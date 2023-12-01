import mysql.connector

class DatabaseManager:

    def get_connection(self):
        # Add your connection details here
        return mysql.connector.connect(user="sql12666408", password="LyqraRUgFf", host="sql12.freesqldatabase.com", database="sql12666408")
