import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

def log_queries(fun):
    """ log the queries which will be passed """
    def wrapper(query):
        print(query)
        return fun(query)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")