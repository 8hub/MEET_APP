# Use an official Python runtime as a parent image
FROM python:3.12.2-slim as base

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for pip install
COPY ./requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django project
COPY . /app/

# Use gunicorn in production
FROM base as production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=MEET_APP.settings

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run entrypoint.sh
COPY ./entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Start gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "MEET_APP.wsgi:application"]
