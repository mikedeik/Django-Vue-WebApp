# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Create a virtual environment and activate it
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

# Install GDAL dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    python3-gdal

RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . .

# Run migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port on which the Django app will run (change if necessary)
EXPOSE 8000

RUN python manage.py collectstatic --no-input

# Define the command to run your Django app using Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
# CMD ["daphne", "-e", "ssl:port=8000:interface=0.0.0.0:privateKey=key.pem:certKey=cert.pem", "backend.asgi:application"]
# Exw kanei allages sto vite.config.ts se sxoleia, sto yarn.lock kai sto package.json