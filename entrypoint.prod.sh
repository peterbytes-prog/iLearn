#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# optional for build
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
# python manage.py collectstatic --noinput
# python manage.py loaddata auth.json
# python manage.py loaddata instructors.json
# python manage.py loaddata students.json
# python manage.py loaddata subjects.json
# python manage.py loaddata courses.json
# python manage.py loaddata others.json
# python manage.py loaddata assignments.json

exec "$@"
