# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 16:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewcourse', '0015_auto_20170322_2036'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='addcourse',
            new_name='course',
        ),
    ]
