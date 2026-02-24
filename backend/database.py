import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="manidhar_ai",
        user="postgres",
        password="Facebooklit@1",
        host="localhost",
        port="5432"
    )