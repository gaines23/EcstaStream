# Generated by Django 3.2.6 on 2022-02-01 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_providers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providers',
            name='logo_path',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='providers',
            name='provider_name',
            field=models.CharField(max_length=150),
        ),
    ]