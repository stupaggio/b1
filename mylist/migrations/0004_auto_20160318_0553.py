# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-18 05:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mylist', '0003_auto_20160309_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='shoplist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mylist.Checklist'),
        ),
    ]