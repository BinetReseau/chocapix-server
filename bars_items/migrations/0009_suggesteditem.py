# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0021_auto_20160117_2034'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bars_items', '0008_auto_20150913_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('added', models.BooleanField(default=False)),
                ('bar', models.ForeignKey(to='bars_core.Bar')),
                ('voters_list', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
