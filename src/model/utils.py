import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")

    # def create_connection(self):
    #     dsn = f"dbname={self.dbname} user={self.user} password={self.password} host={self.host}"
    #     return psycopg2.connect(dsn)

    # @staticmethod
    # def close_connection(connection):
    #     connection.close()

    def get_url():
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

    def create_database(self):
        try:
            conn = psycopg2.connect(dbname="postgres", user=self.user, password=self.password, host=self.host, port=self.port)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(sql.SQL(f"CREATE DATABASE {self.dbname}"))
            cursor.close()
            conn.close()
            print(f"Database {self.dbname} created successfully.")
        except Exception as e:
            print(f"Error creating database: {e}")

    def create_tables(self):
        try:
            conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
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
                overview VARCHAR(100),
                rating FLOAT,
                director VARCHAR(100),
                actors VARCHAR(100)
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


db = Database()
db.create_database()
