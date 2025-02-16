# db_config.py
# import psycopg2

# def get_db_connection():
#     conn = psycopg2.connect(
#     host="localhost",
#     database="api_suite",
#     user="postgres",
#     password="admin"
# )

#     return conn

import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="testdb",
        user="fajrin",
        password="password123"
    )
    return conn
