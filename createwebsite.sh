#!/bin/bash
#
# shell script to init site - run as root
#
# 1. make website folder
# 2. clone project

# create virtual enov

rm -f env
python3 -m venv env
. env/bin/activate

pip install -r requirements.txt

chown -R www-data:peter .
chmod -R g+w .

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic


