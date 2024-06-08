# Generated by Django 5.0.6 on 2024-06-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('constructorId', models.CharField(max_length=64)),
                ('constructorName', models.CharField(max_length=64)),
                ('constructorId2', models.CharField(blank=True, max_length=64)),
                ('constructorId3', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='SeasonResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trackId', models.CharField(max_length=64)),
                ('trackName', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TrackResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
