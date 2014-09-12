#!/bin/sh
python manage.py reset_db
python manage.py syncdb
python manage.py runscript dbdump
