import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
# Make sure you have imported the os module to access environment variables
config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DATABASE'),
}


# Now, you can establish the connection using the config dictionary
cnx = mysql.connector.connect(**config)

# # The rest of the code remains the same
cursor = cnx.cursor()
cursor.execute("SHOW TABLES;")
for table in cursor:
    print(table)
cursor.close()
cnx.close()
