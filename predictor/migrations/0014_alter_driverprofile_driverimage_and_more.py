# Generated by Django 5.0.6 on 2024-06-06 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0013_alter_driverprofile_driverimage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverprofile',
            name='driverImage',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='trackprofile',
            name='trackImage',
            field=models.CharField(max_length=64),
        ),
    ]