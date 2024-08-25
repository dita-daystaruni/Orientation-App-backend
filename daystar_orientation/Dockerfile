# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

#Create a directory for sqlite3,for perisistence
RUN mkdir -p /app/db

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the development server
CMD ["sh", "-c", "python manage.py makemigrations account activities events faqs orientation notifications hods && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
