import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches of size `batch_size`."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_username",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # ✅ using yield

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")


def batch_processing(batch_size):
    """Generator that yields users with age > 25"""
    for batch in stream_users_in_batches(batch_size):     # loop 1
        for user in batch:                                # loop 2
            if user['age'] > 25:
                yield user                                 # ✅ using yield instead of print
