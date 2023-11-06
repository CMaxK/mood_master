#!/bin/bash

# Wait for the MySQL database to be ready
until nc -z -v -w30 db 3306
do
  echo 'Waiting for MySQL...'
  sleep 1
done
echo "MySQL is up and running!"

# Run the command passed to the docker container (e.g., starting Gunicorn)
exec "$@"
