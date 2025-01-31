import psycopg2
from psycopg2 import sql

DB_NAME = "recommender"
DB_USER = "username"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_database():
    try:
        conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql.SQL(f"CREATE DATABASE {DB_NAME}"))
        cursor.close()
        conn.close()
        print(f"Database {DB_NAME} created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")

def create_tables():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(100),
            rating FLOAT
        );
        CREATE TABLE IF NOT EXISTS ratings (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
            score FLOAT NOT NULL
        );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_database()
    # create_tables()
