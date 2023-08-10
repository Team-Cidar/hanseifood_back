#!/bin/bash

# migrate db
python hanseifood/manage.py migrate

# run server
python hanseifood/manage.py runserver 0.0.0.0:8000