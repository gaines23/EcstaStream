# Generated by Django 3.2.6 on 2022-02-01 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_streamingproviderregion_streamingregion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='streamingregion',
            old_name='countryABR',
            new_name='iso_3166_1',
        ),
        migrations.RenameField(
            model_name='streamingregion',
            old_name='country',
            new_name='native_name',
        ),
    ]