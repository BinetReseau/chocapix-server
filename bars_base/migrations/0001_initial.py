# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money', models.FloatField(default=0)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bar', models.ForeignKey(to='bars_core.Bar')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('keywords', models.CharField(max_length=200, blank=True)),
                ('qty', models.FloatField(default=0)),
                ('unit', models.CharField(max_length=100, blank=True)),
                ('unit_value', models.FloatField(default=1)),
                ('buy_unit', models.CharField(max_length=100, blank=True)),
                ('buy_unit_value', models.FloatField(default=1)),
                ('price', models.FloatField()),
                ('buy_price', models.FloatField(default=1)),
                ('deleted', models.BooleanField(default=False)),
                ('unavailable', models.BooleanField(default=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bar', models.ForeignKey(to='bars_core.Bar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('bar', 'owner')]),
        ),
    ]
