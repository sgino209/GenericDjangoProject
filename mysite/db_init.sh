#!/bin/bash
# Reset Flow, be-careful

# Clear:
rm db.sqlite3
rm -rf mysite/__pycache__

# Init:
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb

# Prepare:
python3 manage.py shell < db_init.py

# Run:
python3 manage.py runserver

