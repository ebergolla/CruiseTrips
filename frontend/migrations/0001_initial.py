# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-02 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(help_text=b'The image dimension should be 1680x1050', upload_to=b'uploads')),
                ('order', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CruiseDeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('order', models.PositiveIntegerField()),
                ('expire_date', models.DateField()),
                ('url', models.URLField(default=b'')),
                ('show_in_home', models.BooleanField(default=1, verbose_name=b'Show in Homepage')),
                ('cruise_line', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.CruiseLine')),
            ],
        ),
        migrations.CreateModel(
            name='TopDestination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(help_text=b'The image dimension should be 375x239', upload_to=b'uploads')),
                ('order', models.PositiveIntegerField()),
                ('destination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.SubRegion')),
            ],
        ),
    ]