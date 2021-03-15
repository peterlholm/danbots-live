#!/bin/bash
#
# shell script to init site - run as root
#
# 1. make website folder
# 2. clone project

# create virtual env

rm -rf env
python3 -m venv env
. env/bin/activate

pip install -r requirements_prod.txt

touch db.sqlite3
chmod g+w db.sqlite3
sudo chgrp www-data db.sqlite3

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata common/fixtures/*

python manage.py collectstatic


