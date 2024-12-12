import mysql.connector
import uuid

# Function connects to the mysql database server
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
    )
    
# Function creates the database ALX_prodev if it does not exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()
    
    
# Function to connect to the ALX_prodev database
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    
    
# Function creates a table user_data if it does not exists with the required fields
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5, 2) NOT NULL,
            INDEX (user_id)
        )
    """)
    cursor.close()

    
    
# inserts data in the database if it does not exist
def insert_data(connection, data):
    cursor = connection.cursor()
    query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    cursor.executemany(query, data)
    connection.commit()
    cursor.close()
    
# Function to read data from user_data.csv and prepare it for insertion
def read_csv(file_path):
    import csv
    rows = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rows.append((str(uuid.uuid4()), row['name'], row['email'], float(row['age'])))
        return rows
    
# Main script Logic
if __name__ == "__main__":
    # Connect to the MYSQL Server
    connection = connect_db()
    create_database(connection)
    connection.close
    
    # Connect to the ALX_prodev database
    connection = connect_to_prodev()
    create_table(connection)
    
    #Insert data from CSV
    data  = read_csv('user_data.csv')
    insert_data(connection, data)
    
    print("Database setup and data insertion completed.")
    connection.close()