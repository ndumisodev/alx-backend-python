#!/usr/bin/python3
"""
1-batch_processing.py

This script provides functions for fetching and processing user data
from the 'ALX_prodev' database in batches. It leverages Python generators
to ensure memory efficiency, especially when dealing with large datasets.

Functions:
- stream_users_in_batches(batch_size): A generator that fetches rows
  from the database in specified batch sizes using LIMIT and OFFSET.
- batch_processing(batch_size): A generator that utilizes
  stream_users_in_batches to process each batch, filtering users
  who are over the age of 25.

The script adheres to the constraint of using no more than 3 loops in total.
"""

import seed
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    A generator function that fetches rows from the 'user_data' table
    in the 'ALX_prodev' database in specified batch sizes.

    This function connects to the database and uses SQL's LIMIT and OFFSET
    clauses to retrieve data in chunks. This approach is highly memory-efficient
    as it avoids loading the entire dataset into memory at once.

    Args:
        batch_size (int): The maximum number of rows to fetch in each batch.

    Yields:
        list[dict]: A list of dictionaries, where each dictionary represents
                    a single user row. The list contains up to `batch_size` rows.
                    An empty list is yielded if no more rows are found.
    """
    connection = None
    cursor = None
    offset = 0 # Initialize offset for fetching data
    try:
        # Establish a connection to the 'ALX_prodev' database using the seed module.
        connection = seed.connect_to_prodev()
        if not connection:
            print("Failed to connect to the database. Cannot stream users in batches.")
            return # Exit the generator if connection fails

        # Create a cursor object. `dictionary=True` ensures rows are returned as dictionaries.
        cursor = connection.cursor(dictionary=True)

        # Loop 1 (Primary loop for fetching batches):
        # This loop continues to execute queries and fetch batches until no more
        # rows are returned from the database.
        while True:
            # SQL query to select user data with LIMIT and OFFSET for batching.
            # %s placeholders are used for safe parameter substitution.
            query = "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s"
            cursor.execute(query, (batch_size, offset))

            # Fetch all rows for the current batch. `fetchall()` here is fine
            # as it only fetches `batch_size` rows, not the entire table.
            batch = cursor.fetchall()

            # If the batch is empty, it means there are no more rows in the table.
            if not batch:
                break # Exit the while loop

            # Yield the current batch (a list of user dictionaries).
            yield batch

            # Increment the offset for the next iteration to fetch the next batch.
            offset += batch_size

    except mysql.connector.Error as err:
        print(f"Database error during batch streaming: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during batch streaming: {e}")
    finally:
        # Ensure database resources (cursor and connection) are properly closed.
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    A generator function that processes user data in batches.

    It utilizes the `stream_users_in_batches` generator to receive data
    in chunks. For each batch, it iterates through the users and filters
    them based on the condition that their 'age' is greater than 25.
    Each filtered user is then yielded individually.

    Args:
        batch_size (int): The size of batches to fetch and process.

    Yields:
        dict: A dictionary representing a single user row, but only if
              the user's 'age' is greater than 25.
    """
    # Loop 2 (Iterating over batches):
    # This loop iterates over the batches yielded by `stream_users_in_batches`.
    for batch in stream_users_in_batches(batch_size):
        # Loop 3 (Iterating over users within a batch):
        # This nested loop processes each individual user within the current batch.
        for user in batch:
            # Filter condition: yield user only if age is greater than 25.
            if user['age'] > 25:
                yield user

