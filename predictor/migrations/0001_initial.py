# Generated by Django 5.0.6 on 2024-06-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driverId', models.CharField(max_length=64)),
                ('driverName', models.CharField(max_length=64)),
                ('driverCode', models.CharField(max_length=8)),
                ('driverNumber', models.CharField(max_length=8)),
                ('driverDOB', models.CharField(max_length=64)),
                ('driverNationality', models.CharField(max_length=64)),
                ('constructorId', models.CharField(max_length=64)),
            ],
        ),
    ]
