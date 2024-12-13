import sqlite3
import functools
import logging

#Set up Logging
logging.basicConnfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Decorator to log AQL Queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the SQL before execution
        query = args[0] if args else kwargs.get('query', '')
        logger.ifo(f"Executing SQL Query: {query}")
        
        #Execute the origial function
        return func(*args, **kwargs)
    return wrapper

#Decorator to handlw database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('user.db')
        try:
            result = func(connection, *args, **kwargs)
        finally:
            connection.close()
        return result
    return wrapper

@log_queries
@with_db_connection
def fetch_all_users(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

@with_db_connection
def get_user_by_id(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

#Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")


#Fetch user by ID with automatic conection handling
user = get_user_by_id(user_id=1)
print(user)