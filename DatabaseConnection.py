
import sqlite3

class DatabaseConnection:
    _instance = None

    def __new__(cls, db_path="Abarrotera.db"):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._db_path = db_path
            cls._instance._connection = sqlite3.connect(db_path)
            cls._instance._connection.row_factory = sqlite3.Row
        return cls._instance

    def get_connection(self):
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            DatabaseConnection._instance = None
