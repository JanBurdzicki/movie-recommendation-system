import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

load_dotenv()

# schemas
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class MovieSchema(BaseModel):
    id: int
    title: str
    genre: str
    genre: str
    overview: str
    rating: float
    director: str
    actors: str

class RatingSchema(BaseModel):
    movie_id: int
    rating: float


class Database:
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.engine = None
        self.SessionLocal = None

        self.create_database()
        self.connect()

    def get_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    def create_database(self):
        """Creates the PostgreSQL database if it does not exist."""
        try:
            conn = psycopg2.connect(dbname="postgres", user=self.user, password=self.password, host=self.host, port=self.port)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {self.db_name};")
                # cursor.execute(sql.SQL(f"CREATE DATABASE {self.db_name}"))
                print(f"Database '{self.db_name}' created successfully.")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error creating database: {e}")

    def connect(self):
        """Establishes the database connection using SQLAlchemy."""
        try:
            DATABASE_URL = self.get_url()
            self.engine = create_engine(DATABASE_URL, echo=True)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            print(f"Connected to database '{self.db_name}'")
        except Exception as e:
            print(f"Error establishing connection: {e}")

    def get_session(self):
        """Returns a new database session."""
        return self.SessionLocal()

    def get_db(self):
        """Dependency for getting a database session in FastAPI."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_tables(self, base):
        """Creates tables using the provided SQLAlchemy ORM Base."""
        try:
            base.metadata.create_all(self.engine)
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    overview = Column(String)
    rating = Column(Float)
    director = Column(String)
    actors = Column(String)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float)

    user = relationship("User")
    movie = relationship("Movie")


db = Database()
db.create_tables(Base)
