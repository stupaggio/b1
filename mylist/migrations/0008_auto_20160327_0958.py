# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-27 09:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mylist', '0007_auto_20160320_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='shoplist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mylist.Checklist'),
        ),
        migrations.AlterField(
            model_name='sublist',
            name='sub_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checklists', to=settings.AUTH_USER_MODEL),
        ),
    ]
