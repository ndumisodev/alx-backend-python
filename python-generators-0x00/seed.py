#!/usr/bin/python3
"""
seed.py

This script provides functions to set up and populate a MySQL database named
'ALX_prodev' with user data from a CSV file. It includes functionalities
for connecting to the database, creating the database and table, and
inserting data while ensuring no duplicate entries based on user_id.

Database credentials are expected to be set as environment variables for security.
If not found, default values for local development are used.
"""

import mysql.connector
import csv
import os
import sys # For exiting if critical environment variables are missing

# --- Database Configuration ---
# It's highly recommended to use environment variables for sensitive information.
# For local testing, default values are provided.
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password') # Replace with your MySQL root password

# --- Functions ---

def connect_db():
    """
    Connects to the MySQL database server.

    Returns:
        mysql.connector.connection.MySQLConnection: The connection object if successful,
                                                    None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print(f"Successfully connected to MySQL server at {DB_HOST}")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == mysql.connector.errorcode.CR_CONN_HOST_ERROR:
            print(f"Cannot connect to MySQL host '{DB_HOST}'. Ensure it's running and accessible.")
        else:
            print(f"An unexpected database error occurred: {err}")
        return None

def create_database(connection):
    """
    Creates the 'ALX_prodev' database if it does not already exist.

    Args:
        connection (mysql.connector.connection.MySQLConnection): An active connection
                                                                  to the MySQL server.
    Returns:
        bool: True if the database was created or already exists, False otherwise.
    """
    if not connection:
        print("No active database connection to create database.")
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' created or already exists.")
        return True
    except mysql.connector.Error as err:
        print(f"Error creating database 'ALX_prodev': {err}")
        return False
    finally:
        cursor.close()

def connect_to_prodev():
    """
    Connects to the 'ALX_prodev' database in MySQL.

    Returns:
        mysql.connector.connection.MySQLConnection: The connection object if successful,
                                                    None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database='ALX_prodev'
        )
        print("Successfully connected to 'ALX_prodev' database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to 'ALX_prodev' database: {err}")
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database 'ALX_prodev' does not exist. Please create it first.")
        return None

def create_table(connection):
    """
    Creates the 'user_data' table in the 'ALX_prodev' database if it does not exist.

    Table Schema:
    - user_id (Primary Key, VARCHAR(36), Indexed)
    - name (VARCHAR(255), NOT NULL)
    - email (VARCHAR(255), NOT NULL)
    - age (INT, NOT NULL) - Using INT as age is typically a whole number.

    Args:
        connection (mysql.connector.connection.MySQLConnection): An active connection
                                                                  to the 'ALX_prodev' database.
    Returns:
        bool: True if the table was created or already exists, False otherwise.
    """
    if not connection:
        print("No active database connection to create table.")
        return False

    cursor = connection.cursor()
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age INT NOT NULL
    )
    """
    # Note: PRIMARY KEY automatically creates an index.
    try:
        cursor.execute(table_creation_query)
        connection.commit() # Commit the table creation
        print("Table 'user_data' created successfully or already exists.")
        return True
    except mysql.connector.Error as err:
        print(f"Error creating table 'user_data': {err}")
        return False
    finally:
        cursor.close()

def insert_data(connection, data_file):
    """
    Inserts data from a CSV file into the 'user_data' table.
    It uses INSERT IGNORE to prevent inserting duplicate rows based on the
    PRIMARY KEY (user_id), ensuring data is only added if it doesn't exist.

    Args:
        connection (mysql.connector.connection.MySQLConnection): An active connection
                                                                  to the 'ALX_prodev' database.
        data_file (str): The path to the CSV file containing user data.
    Returns:
        int: The number of rows successfully inserted.
    """
    if not connection:
        print("No active database connection to insert data.")
        return 0

    if not os.path.exists(data_file):
        print(f"Error: CSV file '{data_file}' not found.")
        return 0

    inserted_rows_count = 0
    try:
        cursor = connection.cursor()
        with open(data_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader) # Skip header row

            # Prepare the INSERT IGNORE statement
            # INSERT IGNORE attempts to insert. If a duplicate key (PRIMARY KEY) is found,
            # it simply ignores the row without erroring.
            insert_query = """
            INSERT IGNORE INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """

            for row in csv_reader:
                if len(row) == 4: # Ensure row has expected number of columns
                    try:
                        user_id, name, email, age = row
                        # Convert age to int, handle potential conversion errors
                        age = int(age)
                        cursor.execute(insert_query, (user_id, name, email, age))
                        # Check if a row was actually inserted (not ignored)
                        if cursor.rowcount > 0:
                            inserted_rows_count += 1
                    except ValueError as ve:
                        print(f"Skipping row due to data type error: {row} - {ve}")
                    except mysql.connector.Error as err:
                        # This block will primarily catch errors other than duplicate keys
                        # because INSERT IGNORE handles duplicates silently.
                        print(f"Error inserting row {row}: {err}")
                else:
                    print(f"Skipping malformed row: {row}")

        connection.commit()
        print(f"Data insertion complete. {inserted_rows_count} new rows inserted (duplicates ignored).")
        return inserted_rows_count
    except mysql.connector.Error as err:
        print(f"Database error during data insertion: {err}")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred during data insertion: {e}")
        return 0
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

# Example usage (as seen in 0-main.py, but not executed directly by seed.py)
# This section is for demonstration and testing purposes if you run seed.py directly.
# In the project, it's driven by 0-main.py.
if __name__ == "__main__":
    print("Running seed.py in standalone mode for testing...")
    print("Please ensure MySQL server is running and 'user_data.csv' is in the same directory.")
    print("Set DB_HOST, DB_USER, DB_PASSWORD environment variables if not using defaults.")

    conn_server = connect_db()
    if conn_server:
        if create_database(conn_server):
            conn_server.close() # Close server connection before connecting to specific DB

            conn_prodev = connect_to_prodev()
            if conn_prodev:
                if create_table(conn_prodev):
                    # Create a dummy CSV for testing if not present
                    if not os.path.exists('user_data.csv'):
                        print("Creating dummy 'user_data.csv' for testing...")
                        with open('user_data.csv', 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(['user_id', 'name', 'email', 'age'])
                            writer.writerow(['test-uuid-1', 'Test User 1', 'test1@example.com', 30])
                            writer.writerow(['test-uuid-2', 'Test User 2', 'test2@example.com', 25])
                            writer.writerow(['test-uuid-1', 'Test User 1 Duplicate', 'test1_dup@example.com', 31]) # Duplicate UUID
                        print("Dummy 'user_data.csv' created.")

                    insert_data(conn_prodev, 'user_data.csv')

                    # Verify data
                    cursor = conn_prodev.cursor()
                    cursor.execute("SELECT * FROM user_data LIMIT 5")
                    rows = cursor.fetchall()
                    print("\nFirst 5 rows from user_data table:")
                    for row in rows:
                        print(row)
                    cursor.close()
                conn_prodev.close()
            else:
                print("Failed to connect to 'ALX_prodev' database. Exiting.")
        else:
            print("Failed to create 'ALX_prodev' database. Exiting.")
        conn_server.close() 
        print("Failed to connect to MySQL server. Exiting.")

