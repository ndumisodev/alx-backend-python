#!/usr/bin/python3
"""
2-lazy_paginate.py

This script provides functionality for lazily loading paginated data
from the 'user_data' table in the 'ALX_prodev' MySQL database.
It uses a generator to fetch pages only when they are requested,
optimizing memory usage for large datasets.

Functions:
- paginate_users(page_size, offset): Fetches a single page of user data
  from the database.
- lazy_pagination(page_size): A generator that yields pages of user data
  one by one, fetching them from the database only when needed.
"""

import seed  # To access connect_to_prodev()
import mysql.connector # Required for database error handling (e.g., mysql.connector.Error)

def paginate_users(page_size, offset):
    """
    Fetches one page of users from the database starting at a given offset.

    This function connects to the 'ALX_prodev' MySQL database and retrieves
    a specific page of user data based on the provided `page_size` and `offset`.
    It returns the fetched rows as a list of dictionaries.

    Args:
        page_size (int): The maximum number of rows to fetch for the page.
        offset (int): The starting offset for fetching the page.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents
                    a user row for the requested page. Returns an empty list
                    if no rows are found for the given page and offset.
    """
    connection = None
    cursor = None
    rows = []
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            print("Failed to connect to the database. Cannot paginate users.")
            return []

        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Database error during pagination: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during pagination: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that yields pages of users lazily, one page at a time.

    This generator continuously calls `paginate_users` to fetch pages
    from the database. It yields each page (a list of user dictionaries)
    one by one, only fetching the next page when the current one has been
    consumed. This ensures that only one page is in memory at a time,
    making it highly memory-efficient for very large datasets.

    It adheres to the constraint of having no more than one loop.

    Args:
        page_size (int): The number of users to include in each page.

    Yields:
        list[dict]: A list of dictionaries, where each dictionary represents
                    a user row. Each yielded list is a "page" of data.
    """
    offset = 0
    # Loop 1 (The single loop allowed):
    # This loop continues to fetch and yield pages until an empty page is returned,
    # indicating that there are no more users in the database.
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# Entry point for the script (for testing purposes)
if __name__ == "__main__":
    # Example usage, similar to 3-main.py
    try:
        print("--- Lazily Paginating Users (Page Size: 10) ---")
        page_num = 1
        for page in lazy_pagination(10): # Fetch pages of 10 users
            print(f"\n--- Page {page_num} ---")
            for user in page:
                print(user)
            page_num += 1
            # For demonstration, stop after a few pages, or it will print all users
            if page_num > 3:
                print("\n(Stopped after 3 pages for brevity. Remove this check to print all pages.)")
                break
    except BrokenPipeError:
        # Handles cases where output is piped to a command like `head`
        # and the pipe is closed early.
        import sys
        sys.stderr.close()
    except Exception as e:
        print(f"An error occurred during lazy pagination: {e}")
