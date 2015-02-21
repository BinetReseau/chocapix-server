# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='money_warning_threshold',
            field=models.FloatField(default=15),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bar',
            name='next_scheduled_appro',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
