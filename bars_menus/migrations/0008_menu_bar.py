# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0018_barsettings_default_tax'),
        ('bars_menus', '0007_auto_20150912_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='bar',
            field=models.ForeignKey(default='avironjone', to='bars_core.Bar'),
            preserve_default=False,
        ),
    ]
