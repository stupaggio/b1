# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-20 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mylist', '0005_auto_20160320_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='shoplist',
            field=models.ForeignKey(blank=True, default=60, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mylist.Checklist'),
            preserve_default=False,
        ),
    ]
