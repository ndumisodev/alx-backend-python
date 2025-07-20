import sqlite3 
import functools

def with_db_connection(func):
    """handles opening and closing database connections"""
    def wrapper(user_id, new_email):
        conn = sqlite3.connect('users.db')
        func(conn, user_id, new_email)
        conn.close()

    return wrapper

def transactional(func):
    """ handels the transaction """
    def wrapper(conn, user_id, new_email):
        try:
            func(conn, user_id, new_email)
            conn.commit()
        except sqlite3.Error:
            conn.rollback()
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')