# Generated by Django 5.0.6 on 2024-06-02 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0007_alter_currentseason_avgquali_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentStandings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driverId', models.CharField(blank=True, max_length=64)),
                ('constructorId', models.CharField(blank=True, max_length=64)),
                ('position', models.IntegerField()),
                ('points', models.FloatField()),
            ],
        ),
    ]
