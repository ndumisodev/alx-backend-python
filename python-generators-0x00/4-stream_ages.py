import seed  # Using existing DB connection utility

def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  # ✅ loop 1: yields one age per row
            yield age

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Database error: {e}")


def average_age():
    """Calculates the average age using the stream_user_ages generator."""
    total = 0
    count = 0

    for age in stream_user_ages():  # ✅ loop 2: consume generator
        total += age
        count += 1

    average = total / count if count != 0 else 0
    print(f"Average age of users: {average:.2f}")
