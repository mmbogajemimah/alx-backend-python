import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    
    
# Functio to stream users in batches from the database
def stream_users_in_batches(batch_size):
    connection=connect_db()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM user_data")
    
    while True:
        # Fetch the next batch of rows
        rows = cursor.fetchmany(batch_size)
        
        if not rows:
            break
        
        yield rows
    cursor.close()
    connection.close()
    
    
# Function to process each batch and filter users over the age of 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_batch = [user for user in batch if user['age'] > 25]
        
        yield filtered_batch
        

if __name__ == "__main__":
    batch_size = 5
    
    for processed_batch in batch_processing(batch_size):
        print(processed_batch)