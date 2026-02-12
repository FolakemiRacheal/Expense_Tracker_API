import os
import psycopg2
from psycopg2 import OperationalError

def test_postgres_connection():
    # Update these with your actual database credentials
    DB_CONFIG = {
        'host': 'aws-1-eu-west-1.pooler.supabase.com',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres.wcedcjdleurygyecymil',
        'password': 'gHEHsIL1CVcYVTQc' 
    }
    
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL connection successful!")
        print(f"Database version: {version[0]}")
        cursor.close()
        connection.close()
        return True
    except OperationalError as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_postgres_connection()