#!/bin/sh
# Usage: start.sh <port number>

python /app/manage.py migrate
python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:$1 --chdir=/app
