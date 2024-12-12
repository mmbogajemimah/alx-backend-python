# Getting Started with Python Generators

## Objective  
Create a generator that streams rows from an SQL database one by one.

---

## Instructions  

### 1. Write a Python Script (`seed.py`)  

Set up the MySQL database `ALX_prodev` with the table `user_data` that includes the following fields:  

- **user_id** (Primary Key, UUID, Indexed)  
- **name** (VARCHAR, NOT NULL)  
- **email** (VARCHAR, NOT NULL)  
- **age** (DECIMAL, NOT NULL)  

### 2. Populate the Database  

Use the sample data from `user_data.csv` to populate the database.  

---

## Prototypes  

1. **`connect_db()`**  
   - Connects to the MySQL database server.  

2. **`create_database(connection)`**  
   - Creates the database `ALX_prodev` if it does not exist.  

3. **`connect_to_prodev()`**  
   - Connects to the `ALX_prodev` database in MySQL.  

4. **`create_table(connection)`**  
   - Creates a table `user_data` if it does not exist with the required fields.  

5. **`insert_data(connection, data)`**  
   - Inserts data into the database if it does not exist.  

---  