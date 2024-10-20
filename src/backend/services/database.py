import os
import psycopg2
from contextlib import closing
from dotenv import load_dotenv
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer

# Load environment variables from a specific .env file
load_dotenv(dotenv_path='src/envs/.env')

# Connection details from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')  # Default to localhost if not set
DB_PORT = os.getenv('DB_PORT', '5432')  # Default to 5432 if not set

# Dejavu configuration
dejavu_config = {
    "database": {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME
    },
    "database_type": "postgres"
}

# Initialize Dejavu
djv = Dejavu(dejavu_config)

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
                    fingerprint BYTEA,
                    score FLOAT,
                    date_submitted TIMESTAMP
                )
            ''')
            conn.commit()

def insert_track(url, features, fingerprint, score, date_submitted):
    """Insert a track into the database with fingerprinting and score."""
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO track_cache (url, features, fingerprint, score, date_submitted)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
            ''', (url, psycopg2.Binary(features), psycopg2.Binary(fingerprint), score, date_submitted))
            conn.commit()

def get_track_by_fingerprint(fingerprint):
    """Retrieve a track by its fingerprint."""
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT features, score FROM track_cache WHERE fingerprint = %s', (psycopg2.Binary(fingerprint),))
            row = cursor.fetchone()
            return row if row else None
