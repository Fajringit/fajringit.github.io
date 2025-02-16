import psycopg2
import time

def get_db_connection(retries=5, delay=3):
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                host="postgres",
                database="testdb",
                user="fajrin",
                password="password123"
            )
            return conn
        except Exception as e:
            print(f"Database connection failed (Attempt {attempt+1}): {e}")
            time.sleep(delay)
    raise Exception("Database connection failed after multiple attempts")
