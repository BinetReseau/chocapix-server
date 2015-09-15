# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_menus', '0006_auto_20150911_2052'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('account', 'name')]),
        ),
    ]
