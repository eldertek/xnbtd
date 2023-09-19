#!/bin/sh

export DJANGO_SETTINGS_MODULE=xnbtd.settings.local

exec poetry run python3 manage.py "$@"
