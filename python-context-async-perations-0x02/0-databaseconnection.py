import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        """ Initialize with the database name. """
        self.db_name = db_name
        self.connection = None
        
    def __enter__(self):
        """ Connect to the database when entering a with block. """
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        """ Close the database connection when exiting a with block. """
        if self.connection:
            self.connection.close()
            
       
# Create a sample database with a 'users'     
def setup_database():
    with DatabaseConnection("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.executemany(
            "INSERT INTO users (name) VALUES(?)"
            , [("John",), ("Jane",), ("Bob",)],
        )
        connection.commit()
        

# Query data using the context manager
def query_users():
    with DatabaseConnection("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
            
            
# Set up the database and test the context manager
setup_database()
query_users()