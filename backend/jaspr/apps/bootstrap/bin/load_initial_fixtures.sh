#!/bin/bash

python manage.py migrate

echo "loading aws media group"
python manage.py load_fixtures media

echo "loading content group"
python manage.py load_fixtures content

echo "loading dev_only group"
python manage.py load_fixtures dev_only

echo "loading user group"
python manage.py load_fixtures user
