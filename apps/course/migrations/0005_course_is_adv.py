# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-31 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_adv',
            field=models.BooleanField(default=False, verbose_name='是否是广告位'),
        ),
    ]
