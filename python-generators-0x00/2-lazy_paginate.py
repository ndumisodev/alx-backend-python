import seed  # To access connect_to_prodev()

def paginate_users(page_size, offset):
    """Fetches one page of users from the database starting at a given offset."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator that yields pages of users lazily, one page at a time."""
    offset = 0
    while True:  # Only ONE loop used
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
