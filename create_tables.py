import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# SQL queries to create tables
CREATE_RESULTS_TABLE = '''
CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    rollNumber VARCHAR(100),
    score INTEGER,
    total INTEGER,
    percentage INTEGER,
    timeSpent INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    results TEXT
);
'''

CREATE_INDEX_QUERY = '''
CREATE INDEX IF NOT EXISTS idx_rollNumber ON results(rollNumber);
CREATE INDEX IF NOT EXISTS idx_timestamp ON results(timestamp DESC);
'''

# Connect to the database and create tables
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("✓ Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Create the results table
    cursor.execute(CREATE_RESULTS_TABLE)
    print("✓ Table 'results' created successfully!")
    
    # Create indexes for better performance
    cursor.execute(CREATE_INDEX_QUERY)
    print("✓ Indexes created successfully!")
    
    # Commit the changes
    connection.commit()
    
    # Verify table creation
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'results'
        ORDER BY ordinal_position;
    """)
    columns = cursor.fetchall()
    
    print("\n📋 Table Structure:")
    print("-" * 50)
    for column in columns:
        print(f"  {column[0]:<20} {column[1]}")
    print("-" * 50)
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("\n✓ Setup completed successfully!")
    print("✓ Connection closed.")

except Exception as e:
    print(f"❌ Failed to create tables: {e}")
