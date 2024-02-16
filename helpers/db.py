import os
import mysql.connector
from dotenv import load_dotenv
from pandas import read_sql_query
from log import setup_logger

log = setup_logger()
load_dotenv()

def get_db_connection():
    try:
        log.info("Attempting to connect to the database.")
        db = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB')
        )
        return db
    except Exception as e:
        log.error(f"Error connecting to the database: {e}")
        raise

def load_from_db():
    db = get_db_connection()
    query = """
        SELECT *
        FROM input_data;
    """
    result = read_sql_query(query, con=db)
    return result

if __name__ == "__main__":
    try:
        # Attempt to establish a database connection
        db_connection = get_db_connection()

        # If the connection was successful, print a success message
        if db_connection:
            print("Database connection established successfully!")
            # Perform additional operations if needed
        else:
            print("Failed to establish a database connection.")
    except Exception as e:
        print(f"An error occurred: {e}")
