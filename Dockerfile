# Base image with Python 3.9 installed
FROM python:3.9

# Set the working directory
WORKDIR /app

COPY setup.py /app/setup.py
# Copy the package code into the container
COPY requirements.txt /app/requirements.txt
# Install package requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src
COPY pytest.ini app/pytest.ini

# Copy the package code into the container

