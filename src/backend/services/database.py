import os
import psycopg2
from contextlib import closing
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='envs/.env')


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def initialize_db():
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS track_cache (
                    id SERIAL PRIMARY KEY,
                    url TEXT UNIQUE,
                    features BYTEA,
                    score FLOAT,
                    date_submitted TIMESTAMP
                )
            ''')
            conn.commit()

def insert_track(url, features, score, date_submitted):
    """Insert a track into the database."""
    
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO track_cache (url, features, score, date_submitted)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
            ''', (url, psycopg2.Binary(features), score, date_submitted))
            conn.commit()