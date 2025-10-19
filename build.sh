#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Clear migration history and rerun
python manage.py migrate --fake-initial
python manage.py migrate --run-syncdb

python manage.py create_default_superuser