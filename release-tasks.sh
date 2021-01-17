#!/bin/bash

python manage.py migrate
mkdir -p ${STATIC_ROOT}
python manage.py collectstatic --noinput
