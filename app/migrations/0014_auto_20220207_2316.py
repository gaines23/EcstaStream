# Generated by Django 3.2.6 on 2022-02-08 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20220204_1240'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='collection',
            table='app_collection',
        ),
        migrations.AlterModelTable(
            name='genre',
            table='app_genre',
        ),
        migrations.AlterModelTable(
            name='streamingregion',
            table='app_streamingregion',
        ),
        migrations.AlterModelTable(
            name='streamingservices',
            table='app_streamingservices',
        ),
        migrations.AlterModelTable(
            name='uscerts',
            table='app_uscerts',
        ),
    ]