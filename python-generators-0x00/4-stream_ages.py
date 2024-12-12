import mysql.connector

def conect_db():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database="ALX_prodev"
    )
    
    
# Generator function to stream user ages one by one
def stream_user_ages():
    connection = conect_db()
    cursor = connection.cursor(dictionary=True)
    
    # Query to fetch all user data
    cursor.execute("SELECT age from user_data")
    
    for row in cursor:
        yield row['age']
        
    cursor.close()
    connection.close()
    
# Function to calculate the average age of users
def calculate_average_age():
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
        
    # Calculate the average age
    if count > 0:
        average_age = total_age/count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found.")
        
        
        
if __name__ == "__main__":
    calculate_average_age()