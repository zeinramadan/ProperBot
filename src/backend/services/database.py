import os
import psycopg2
from psycopg2 import sql
from contextlib import closing
from dotenv import load_dotenv

# Load environment variables from a specific .env file
load_dotenv(dotenv_path='src/envs/.env')

# Connection details from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')  # Default to localhost if not set
DB_PORT = os.getenv('DB_PORT', '5432')  # Default to 5432 if not set

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def initialize_db():
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS track_cache (
                    id SERIAL PRIMARY KEY,
                    url TEXT UNIQUE,
                    features BYTEA,
                    date_submitted TIMESTAMP
                )
            ''')
            conn.commit()

def insert_track(url, features, date_submitted):
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO track_cache (url, features, date_submitted)
                VALUES (%s, %s, %s)
                ON CONFLICT (url) DO NOTHING
            ''', (url, psycopg2.Binary(features), date_submitted))
            conn.commit()

def get_track(url):
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT features FROM track_cache WHERE url = %s', (url,))
            row = cursor.fetchone()
            return row[0] if row else None
