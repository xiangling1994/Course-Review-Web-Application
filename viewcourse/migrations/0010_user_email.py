# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewcourse', '0009_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='null', max_length=30),
        ),
    ]