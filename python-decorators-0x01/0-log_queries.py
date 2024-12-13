import sqlite3
import functools
import logging

#Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the SQL query before execution
        query = args[0] if args else kwargs.get('query', '')
        logger.info(f"Executing SQL query: {query}")
        
        #Exwcute the original function
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")

