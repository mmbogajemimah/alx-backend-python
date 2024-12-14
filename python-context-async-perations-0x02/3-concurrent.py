import aiosqlite
import asyncio

async def setup_database():
    async with aiosqlite.connect("users2.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Alice", 22), ("Bob", 30), ("Charlie", 45), ("Diana", 50)],
        )
        await db.commit()
        
# Create two asynchronous functions for fetching data
async def async_fetch_users():
    async with aiosqlite.connect("users2.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        return results
    
    
async def async_fetch_older_users():
    async with aiosqlite.connect("users2.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        await cursor.close()
        return results
    
    
async def fetch_concurrently():
    """
    Run multiple queries concurretly
    """
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )
    
    print("All Users:")
    for user in results[0]:
        print(user)
        
    print("\nUsers Older than 40:")
    for user in results[1]:
        print(user)
        


if __name__ == "__main__":
    # Setup the database and run concurrent queries
    asyncio.run(setup_database()) 
    asyncio.run(fetch_concurrently())
  
        