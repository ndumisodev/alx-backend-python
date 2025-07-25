import sqlite3 
import functools

def with_db_connection(func):
    """handles opening and closing database connections""" 
    def wrapper(user_id):
        conn = sqlite3.connect('users.db')
        users = func(conn, user_id)
        conn.close()
        return users
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
    #### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)