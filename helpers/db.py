import os
import mysql.connector
from dotenv import load_dotenv, find_dotenv
from pandas import read_sql_query

env_path = find_dotenv()
load_dotenv(env_path)

def get_db_connection():
    db = mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST'),
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        database=os.environ.get('MYSQL_DB')
    )
    return db

def load_from_db():
    db = get_db_connection()
    query = """
        SELECT *
        FROM input_data;
    """
    result = read_sql_query(query, con=db)
    return result
