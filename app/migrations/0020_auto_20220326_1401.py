# Generated by Django 2.1.15 on 2022-03-26 21:01

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20220326_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritelist',
            name='favorites',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
