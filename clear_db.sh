#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

find . -iname 000* | xargs rm -f
/usr/bin/python `dirname $0`/manage.py flush
rm db.sqlite3
./manage.sh makemigrations 
./manage.sh migrate
