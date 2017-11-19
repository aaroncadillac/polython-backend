# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 08:24
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_auto_20171119_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='products',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[{'id': 'a6cae661-ac03-467b-92da-1182b1c943c8', 'name': 'demo_product', 'price': 50, 'quantity': 5}]),
        ),
    ]