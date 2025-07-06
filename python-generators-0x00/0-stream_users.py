#!/usr/bin/python3
"""
0-stream_users.py

This script defines a generator function `stream_users` that fetches
rows from the 'user_data' table in the 'ALX_prodev' MySQL database
one by one. It yields each row as a dictionary, making it memory-efficient
for large datasets.

It reuses the database connection functionality from the `seed` module.
"""

# Import the seed module to utilize its database connection functions.
# Ensure seed.py is in the same directory or accessible via PYTHONPATH.
import seed
import mysql.connector

def stream_users():
    """
    A generator function that streams rows from the 'user_data' table
    in the 'ALX_prodev' database. Each row is yielded as a dictionary.

    This function ensures memory efficiency by fetching and yielding
    one row at a time, making it suitable for large datasets.
    It adheres to the constraint of having no more than one loop.

    Yields:
        dict: A dictionary representing a single user row, with keys
              corresponding to column names (user_id, name, email, age).
    """
    connection = None
    cursor = None
    try:
        # Establish a connection to the 'ALX_prodev' database.
        # This function is defined in seed.py.
        connection = seed.connect_to_prodev()
        if not connection:
            print("Failed to connect to the database. Cannot stream users.")
            return # Exit the generator if connection fails

        # Create a cursor object to execute SQL queries.
        cursor = connection.cursor(dictionary=True) # dictionary=True makes rows return as dicts

        # Execute the query to select all data from the user_data table.
        # The cursor will fetch results lazily when iterated over.
        query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(query)

        # Iterate directly over the cursor, which acts as an iterator.
        # This is the single loop allowed. Each iteration fetches one row.
        for row in cursor:
            yield row # Yield the row (which is already a dictionary)

    except mysql.connector.Error as err:
        print(f"Database error during streaming: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the cursor and connection are closed, regardless of success or failure.
        if cursor:
            cursor.close()
            # print("Cursor closed.") # For debugging
        if connection:
            connection.close()
            # print("Connection closed.") # For debugging

