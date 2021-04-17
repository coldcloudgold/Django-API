#! /bin/sh


sleep 15


python3 manage.py makemigrations


python3 manage.py migrate


python3 manage.py loaddata fixtures/initial_data.json


python3 manage.py collectstatic


python3 manage.py rqworker & python3 manage.py rqscheduler & gunicorn API_project.wsgi:application -b 0.0.0.0:8000 --reload
