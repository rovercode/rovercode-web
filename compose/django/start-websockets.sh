#!/bin/sh
# Usage: start.sh <port number>

python /app/manage.py migrate
python /app/manage.py collectstatic --noinput
/usr/local/bin/daphne -b 0.0.0.0 -p $1 config.asgi:application
