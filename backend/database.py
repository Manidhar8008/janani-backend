import psycopg2
import os

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Use DATABASE_URL if provided (Railway)
        return psycopg2.connect(database_url)
    else:
        # Fall back to local development
        return psycopg2.connect(
            dbname="manidhar_ai",
            user="postgres",
            password="Facebooklit@1",
            host="localhost",
            port="5432"
        )