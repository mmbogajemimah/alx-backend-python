import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, parameters=None):
        """
        Initialize the context manager with the database name, query, and parameters.
        """
        self.db_name = db_name
        self.query = query
        self.parameters = parameters or []  # Default to an empty list if no parameters provided
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Open the database connection and prepare for query execution.
        """
        # Open the database connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self  # Return the instance for further query execution

    def execute(self):
        """
        Execute the query with the provided parameters and return results.
        """
        self.cursor.execute(self.query, self.parameters)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensure the connection is closed.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

            
            
def setup_database():
    """Create a sample database with a 'users' table for testing."""
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Alice", 22), ("Bob", 30), ("Charlie", 35), ("Diana", 28)],
        )
        conn.commit()


if __name__ == "__main__":
    # Setup the database (this is for demonstration purposes)
    setup_database()

    # Define the query and parameters
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    # Use the ExecuteQuery context manager to run the query
    with ExecuteQuery("users.db", query, params) as executor:
        results = executor.execute()
        for row in results:
            print(row)
