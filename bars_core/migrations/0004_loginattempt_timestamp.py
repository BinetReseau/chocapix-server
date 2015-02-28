# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0003_loginattempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginattempt',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 28, 17, 27, 42, 151381, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
