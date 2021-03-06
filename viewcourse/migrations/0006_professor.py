# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 23:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewcourse', '0005_auto_20170307_0559'),
    ]

    operations = [
        migrations.CreateModel(
            name='professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=20)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=2)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professors', to='viewcourse.addcourse')),
            ],
        ),
    ]
