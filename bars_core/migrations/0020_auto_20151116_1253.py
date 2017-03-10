# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0019_auto_20151116_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('policeman', 'policeman'), ('usermanager', 'usermanager'), ('stockmanager', 'stockmanager'), ('itemmanager', 'itemmanager'), ('staff', 'staff'), ('admin', 'admin'), ('inventorymanager', 'inventorymanager'), ('barmanager', 'barmanager'), ('appromanager', 'appromanager'), ('usercreator', 'usercreator'), ('agios_daemon', 'agios_daemon'), ('customer', 'customer'), ('newsmanager', 'newsmanager'), ('accountmanager', 'accountmanager'), ('itemcreator', 'itemcreator'), ('treasurer', 'treasurer')], max_length=127),
        ),
        migrations.AlterField(
            model_name='user',
            name='current_login',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='previous_login',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
