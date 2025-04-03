import os
import psycopg2

# Get environment variables from GitHub Actions
host = os.getenv("POSTGRES_HOST", "localhost")
port = os.getenv("POSTGRES_PORT", "5432")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "1")
database = os.getenv("POSTGRES_DB", "testdb")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()

    # Example Query: Create Table
    cursor.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name TEXT);")
    conn.commit()

    print("Table created successfully.")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"Database connection error: {e}")