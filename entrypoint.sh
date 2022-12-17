#!/usr/bin/env bash

if [ "$DATABASE" = "mongodb" ]
then
    echo "Waiting for mongodb clusters..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "MongoDB started"
fi

python src/main.py

exec "$@"