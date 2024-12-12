import mysql.connector

# Function to connect to the MYSQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    
# Function to fetch a page of users with the given page size and offset
def paginate_users(page_size, offset):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    
    #Query to fetch users based on LIMIT and OFFSET
    query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

# Lazy pagination generator function
def lazy_paginate(page_size):
    offset = 0
    while True:
        # Fetch the next page of users
        users = paginate_users(page_size, offset)
        
        # if there are no more users stop the generator
        if not users:
            break
        
        yield users
        
        # Increment the offset by page_size for the next page
        offset += page_size


# Function to process and display paginated data
def process_paginated_data():
    page_size = 10
    for page in lazy_paginate(page_size):
        print(f"Processing page of {len(page)} users...")
        for user in page:
            print(user)


if __name__ == "__main__":
    process_paginated_data()