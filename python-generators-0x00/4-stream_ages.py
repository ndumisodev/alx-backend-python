#!/usr/bin/python3
"""
4-stream_ages.py

This script demonstrates memory-efficient aggregation using Python generators.
It calculates the average age of users from the 'user_data' table without
loading the entire dataset into memory.

Functions:
- stream_user_ages(): A generator that yields user ages one by one.
- average_age(): Calculates the average age by consuming the `stream_user_ages` generator.
"""

import seed
import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the 'user_data' table in the database.

    This generator connects to the 'ALX_prodev' MySQL database and fetches
    the 'age' column for all users. It yields each age individually,
    making it highly memory-efficient for large datasets by avoiding
    loading all ages into memory at once.

    Yields:
        int: The age of a single user.

    Raises:
        mysql.connector.Error: If a database-related error occurs during connection or query.
        Exception: For any other unexpected errors during the streaming process.
    """
    connection = None
    cursor = None
    try:
        # Establish a connection to the 'ALX_prodev' database.
        connection = seed.connect_to_prodev()
        if not connection:
            print("Failed to connect to the database. Cannot stream user ages.")
            return # Exit the generator if connection fails

        # Create a cursor object. We don't need dictionary=True here
        # as we are only fetching a single column ('age').
        cursor = connection.cursor()

        # Execute the query to select only the 'age' column.
        query = "SELECT age FROM user_data"
        cursor.execute(query)

        # Loop 1: Iterate directly over the cursor to fetch ages one by one.
        for (age,) in cursor: # Unpack the single-element tuple (age,)
            yield age # Yield the age

    except mysql.connector.Error as err:
        print(f"Database error during age streaming: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure database resources (cursor and connection) are properly closed.
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def average_age():
    """
    Calculates the average age of users using the stream_user_ages generator.

    This function consumes ages yielded by the `stream_user_ages` generator
    one by one, accumulating the total age and count of users without
    storing all ages in memory. This approach is memory-efficient for
    large datasets.

    The calculated average age is printed to the console, formatted to
    two decimal places. It handles the case where no users are found
    to prevent division by zero errors.

    Prints:
        str: A string indicating the calculated average age, or a message
             if no users are found.
    """
    total = 0
    count = 0

    # Loop 2: Iterate over the ages yielded by the generator.
    # This loop consumes ages one by one as they are generated,
    # preventing the entire dataset from being stored in memory.
    for age in stream_user_ages(): #  loop 2: consume generator
        total += age
        count += 1

    # Calculate the average age. Handle division by zero if no users are found.
    average = total / count if count != 0 else 0
    print(f"Average age of users: {average:.2f}")

# Entry point for the script
if __name__ == "__main__":
    average_age()

