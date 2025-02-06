# Recommendation System project for LLM course

## Prerequisites

Ensure you have the following installed on your system:
* Python 3
* PostgreSQL

## Setting Up the Database

1. Switch to the PostgreSQL user:
   ```sh
   sudo -i -u postgres
   ```
2. Access PostgreSQL:
   ```sh
   psql
   ```
3. Create a new user with superuser privileges:
   ```sql
   CREATE USER username WITH SUPERUSER PASSWORD 'password';
   ```

## Configuring Environment Variables

Create a `.env` file in the root directory and add the following configurations:

```env
DB_NAME = "recommender"
DB_USER = "username"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

Note: Modify `.env` with actual credentials if needed.


## Running the Application
1. Initialize the database:
   ```sh
   python3 src/model/utils.py
   ```
2. Start the application:
   ```sh
   python3 src/main.py
   ```
