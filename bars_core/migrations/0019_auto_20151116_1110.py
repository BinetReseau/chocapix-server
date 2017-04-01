# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0018_barsettings_default_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_login',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 16, 11, 10, 53, 54292, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='previous_login',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 16, 11, 10, 58, 214627, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('barmanager', 'barmanager'), ('admin', 'admin'), ('stockmanager', 'stockmanager'), ('customer', 'customer'), ('itemmanager', 'itemmanager'), ('staff', 'staff'), ('usercreator', 'usercreator'), ('itemcreator', 'itemcreator'), ('inventorymanager', 'inventorymanager'), ('treasurer', 'treasurer'), ('appromanager', 'appromanager'), ('agios_daemon', 'agios_daemon'), ('policeman', 'policeman'), ('accountmanager', 'accountmanager'), ('usermanager', 'usermanager'), ('newsmanager', 'newsmanager')], max_length=127),
        ),
    ]
