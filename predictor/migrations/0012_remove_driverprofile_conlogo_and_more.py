# Generated by Django 5.0.6 on 2024-06-05 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0011_remove_driverprofile_title_driverprofile_conlogo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverprofile',
            name='conLogo',
        ),
        migrations.RemoveField(
            model_name='driverprofile',
            name='flag',
        ),
        migrations.RemoveField(
            model_name='driverprofile',
            name='signature',
        ),
        migrations.RemoveField(
            model_name='trackprofile',
            name='flag',
        ),
        migrations.RemoveField(
            model_name='trackprofile',
            name='trackMap',
        ),
        migrations.AddField(
            model_name='driverprofile',
            name='driverImage',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trackprofile',
            name='trackImage',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]