# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-03 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0010_auto_20160403_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='id',
            field=models.UUIDField(default='9ec5b06b61334ecb80c866111e5688cb', editable=False, primary_key=True, serialize=False),
        ),
    ]
