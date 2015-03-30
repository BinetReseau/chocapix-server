# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def split_full_name(apps, schema_editor):
    User = apps.get_model("bars_core", "User")
    for user in User.objects.all():
        x = user.full_name.split(" ")
        try:
            user.first_name = x[0]
            user.last_name = x[1]
        except IndexError:
            pass
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0013_auto_20150329_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(split_full_name),
        migrations.RemoveField(
            model_name='user',
            name='full_name',
        ),
    ]
