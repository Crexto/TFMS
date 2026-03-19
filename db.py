import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            database="tfms",
            user="postgres",
            password="charith",
            host="127.0.0.1",
            port=5432,
        )
        print("Connection to PostgreSQL established successfully.")
        return conn
    except Exception as err:
        print("Error connecting to PostgreSQL:", err)
        return None

conn = get_connection()