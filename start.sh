#!/bin/bash

# make migrations
#python hanseifood/manage.py makemigrations food

# migrate db
python hanseifood/manage.py migrate

# run server
python hanseifood/manage.py runserver --noreload 0:8000