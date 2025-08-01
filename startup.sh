#!/bin/bash

export FLASK_APP=run.py
export FLASK_ENV=production

gunicorn --bind=0.0.0.0 --timeout 600 run:app
