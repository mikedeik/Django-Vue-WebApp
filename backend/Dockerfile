# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . .

# Expose the port on which the Django app will run (change if necessary)
EXPOSE 8000

# Start the Redis container as a service
RUN docker run -d -p 6379:6379 redis:5

# Define the command to run your Django app using Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
