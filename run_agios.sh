#!/bin/sh
LOGFILE=/srv/api/cron.log

cd /app
date >> $LOGFILE
python manage.py runscript agios >> $LOGFILE 2>&1
