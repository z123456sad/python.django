# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-21 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180119_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='send_type',
            field=models.CharField(choices=[('register', '注册验证码'), ('forget', '忘记验证码')], max_length=10),
        ),
    ]
