# Generated by Django 5.0.6 on 2024-06-01 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_constructor_seasonresults_track_trackresults'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SeasonResults',
            new_name='SeasonResult',
        ),
        migrations.RenameModel(
            old_name='TrackResults',
            new_name='TrackResult',
        ),
        migrations.AddField(
            model_name='track',
            name='trackCity',
            field=models.CharField(default='null', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='track',
            name='trackCountry',
            field=models.CharField(default='null', max_length=64),
            preserve_default=False,
        ),
    ]
