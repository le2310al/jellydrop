#import sqlite3
#import psycopg2
"""
# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
except Exception as e:
    print(f"Failed to connect: {e}")
"""
"""
cursor.execute(
    "INSERT INTO jellies (name, url , stock, availability, last_updated) "
    + "VALUES('" + name + "' ,'" + url + "' , stock, '" + availability + "', NOW() ) "
    + "ON CONFLICT (name) DO UPDATE SET availability = EXCLUDED.availability ;"
)

connection.commit()

    cursor.close()
    connection.close()
"""

# Connect to PostgreSQL database
# connection = psycopg2.connect("dbname=jellydrop user=postgres")

# Create a SQLite database
# connection = sqlite3.connect("stock_status.sqlite")

# cursor.execute("CREATE TABLE IF NOT EXISTS jellies(id TEXT PRIMARY KEY , url TEXT NOT NULL, availability TEXT NOT NULL)")