#!/bin/bash

# PDM initialization
pdm install
eval "$(pdm --pep582)"

# Alias creation
echo 'alias manage="python manage.py"' >> ~/.zshrc
echo 'alias admin="django-admin"' >> ~/.zshrc

# Python server initialization (Django)
# python manage.py runserver 0.0.0.0:8000
tail -f /dev/null