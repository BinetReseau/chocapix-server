# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=128)),
                ('full_name', models.CharField(max_length=128, blank=True)),
                ('pseudo', models.CharField(max_length=128, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('next_scheduled_appro', models.DateTimeField(null=True)),
                ('money_warning_threshold', models.FloatField(default=15)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127, choices=[(b'customer', b'customer'), (b'moneymanager', b'moneymanager'), (b'policeman', b'policeman'), (b'admin', b'admin'), (b'inventorymanager', b'inventorymanager'), (b'appromanager', b'appromanager'), (b'newsmanager', b'newsmanager'), (b'accountmanager', b'accountmanager'), (b'staff', b'staff')])),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bar', models.ForeignKey(to='bars_core.Bar')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
