import sqlite3


class DatabaseConnection():
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """ initate the connection with database """
        self.connection = sqlite3.connect('users.db')
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()

with DatabaseConnection() as obj:
    cursor = obj.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())