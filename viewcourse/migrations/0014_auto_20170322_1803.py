# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewcourse', '0013_auto_20170322_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingcriteria',
            name='clarity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='ratingcriteria',
            name='easiness',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='ratingcriteria',
            name='helpfulness',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='ratingcriteria',
            name='textbook',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
    ]