# Generated by Django 3.2.6 on 2022-02-02 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20220201_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movieid', models.IntegerField(primary_key=True, serialize=False)),
                ('adult', models.BooleanField()),
                ('budget', models.IntegerField()),
                ('imdbid', models.IntegerField()),
                ('orginal_language', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=500)),
                ('release_date', models.DateField()),
                ('revenue', models.IntegerField()),
                ('runtime', models.IntegerField()),
                ('tagline', models.CharField(max_length=200)),
                ('collection', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.collection')),
            ],
        ),
    ]