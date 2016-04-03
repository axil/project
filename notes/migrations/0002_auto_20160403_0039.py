# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-03 00:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2016, 4, 3, 0, 39, 22, 172209, tzinfo=utc), unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notes',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
