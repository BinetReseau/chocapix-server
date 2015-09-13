# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bars_menus', '0008_menu_bar'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='user',
            field=models.ForeignKey(default=4, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('bar', 'user', 'name')]),
        ),
        migrations.RemoveField(
            model_name='menu',
            name='account',
        ),
    ]
