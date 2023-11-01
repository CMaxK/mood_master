# Use an official Python runtime as the base image
FROM python:3.10.6

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Command
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
