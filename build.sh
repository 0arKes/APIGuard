#!/usr/bin/env bash
set -o errexit

poetry install --no-interaction --no-ansi --no-root
poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate