# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-05 01:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=30)),
                ('list_code', models.CharField(max_length=30)),
                ('list_mkr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=40)),
                ('comment', models.CharField(max_length=140)),
                ('qty', models.IntegerField(default=1)),
                ('shop', models.CharField(max_length=40)),
                ('shoplist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mylist.Checklist')),
            ],
        ),
        migrations.CreateModel(
            name='Sublist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mylist.Checklist')),
                ('sub_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
