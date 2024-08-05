# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to prevent Python from writing pyc files(Compiled Python files) to the container for more lightweightness
ENV PYTHONDONTWRITEBYTECODE = 1
# Set environment variables to prevent Python from buffering the output to the container for more lightweightness
ENV PYTHONUNBUFFERED = 1

# Set the working directory in the container
WORKDIR /app

#Create a directory for sqlite3
RUN mkdir -p /app/db

# Copy the requirements file to the container
COPY requirements.txt .

# Create and activate the virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Run migrations to create the database schema
RUN python3 manage.py makemigrations account activities events faqs orientation
RUN python3 manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Command to run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
