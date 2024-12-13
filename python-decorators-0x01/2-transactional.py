import sqlite3
import functools
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the SQL query before execution
        query = args[0] if args else kwargs.get('query', '')
        logger.info(f"Executing SQL Query: {query}")

        # Execute the original function
        return func(*args, **kwargs)

    return wrapper

# Decorator to handle database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open database connection
        try:
            result = func(conn, *args, **kwargs)  # Pass connection to the wrapped function
        finally:
            conn.close()  # Ensure the connection is closed
        return result
    return wrapper

# Decorator to handle transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(connection, *args, **kwargs):
        try:
            result = func(connection, *args, *kwargs)
            connection.commit()  # Commit the transaction
            return result
        except Exception as e:
            connection.rollback()
            logger.error(f"Transaction failes: {e}")
            raise
    return wrapper

@log_queries
@with_db_connection
def fetch_all_users(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

@with_db_connection
@transactional
def update_user_email(connection, user_id, new_email):
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    return cursor.fetchone()

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')