import sqlite3


class ExecuteQuery():
    def __init__(self, query, parameter):
        self.connection = None
        self.query = query
        self.parameter = parameter

    def __enter__(self):
        """ initate the connection with database """
        self.connection = sqlite3.connect('users.db')
        cursor = self.connection.cursor()
        cursor.execute(self.query, (self.parameter,))
        return cursor.fetchall()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()

with ExecuteQuery("SELECT * FROM users WHERE age > ?", 25) as obj:
    print(obj)