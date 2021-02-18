#!/bin/sh

gunicorn --workers=2 --bind=0.0.0.0:8000 app.wsgi:application --capture-output