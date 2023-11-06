import os
from dotenv import find_dotenv, load_dotenv

env_path = find_dotenv()
if not env_path:
    raise Exception("Can't find .env file")

load_dotenv(env_path)

# Immediately after loading, check if the variable is present
host = os.getenv('MYSQL_HOST')
if host is None:
    raise Exception("MYSQL_HOST not found in .env file")
else:
    print(f"MYSQL_HOST is set to {host}")
