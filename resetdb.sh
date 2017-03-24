#!/bin/sh
python manage.py reset_db && \
python manage.py migrate && \
python manage.py runscript dbdump
