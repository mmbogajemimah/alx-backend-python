import mysql.connector

#Function to connect to the MYSQL Database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    
#Generaror to stream Users oneby one
def stream_users():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    
    #Execute the SELECT QUERY TO SELECT ALL USERS
    cursor.execute("SELECT * FROM user_data")
    
    # Fetch each row one by one and yield it
    for row in cursor:
        yield row
        
    # Closing the Cursor and connection
    cursor.close()
    connection.close()
    

if __name__ == "__main__":
    # Stream users and print each one
    for user in stream_users():
        print(user)