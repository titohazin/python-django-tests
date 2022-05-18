#!/bin/bash

# PDM initialization
pdm install
eval "$(pdm --pep582)"
echo 'export PATH=$PATH:/home/python/app/__pypackages__/3.10/bin' >> ~/.zshrc
echo 'export PATH=$PATH:/home/python/app/__pypackages__/3.10/bin' >> ~/.bashrc

# Alias creation
echo 'alias manage="python manage.py"' >> ~/.zshrc
echo 'alias admin="django-admin"' >> ~/.zshrc

# Python server initialization (Django)
# python manage.py runserver 0.0.0.0:8000
tail -f /dev/null