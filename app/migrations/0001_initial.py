# Generated by Django 3.2.6 on 2022-04-11 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('summary', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'app_collection',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('genre', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'app_genre',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StreamingRegion',
            fields=[
                ('iso_3166_1', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('native_name', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'app_streamingregion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StreamingServices',
            fields=[
                ('provider_id', models.IntegerField(primary_key=True, serialize=False)),
                ('display_priority', models.IntegerField(blank=True, null=True)),
                ('logo_path', models.CharField(blank=True, max_length=200, null=True)),
                ('provider_name', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'app_streamingservices',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Streamingurls',
            fields=[
                ('provider_id', models.IntegerField(primary_key=True, serialize=False)),
                ('url_path', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'app_streamingurls',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsCerts',
            fields=[
                ('us_certsid', models.AutoField(primary_key=True, serialize=False)),
                ('certification', models.CharField(blank=True, max_length=10, null=True)),
                ('meaning', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'app_uscerts',
                'managed': False,
            },
        ),
    ]
