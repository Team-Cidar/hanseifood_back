#!/bin/bash

# make migrations
#python hanseifood/manage.py makemigrations food

# migrate db
python manage.py migrate

# run server
python manage.py runserver 0.0.0.0:8000 --noreload