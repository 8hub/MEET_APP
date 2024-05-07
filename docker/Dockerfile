# Use the official Python image
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL development files
RUN apt-get update \
    && apt-get install -y libpq-dev

# Copy only the necessary files for pip install
COPY ../requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django project
COPY ../ /app/

# Set environment variables for Django to run in development
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=MEET_APP.settings

# Expose the port the app runs on
EXPOSE 8000

# Command to start your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
