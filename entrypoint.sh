#!/bin/bash
echo "Making migrations and migrating the database."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Execute the passed command
exec "$@"
