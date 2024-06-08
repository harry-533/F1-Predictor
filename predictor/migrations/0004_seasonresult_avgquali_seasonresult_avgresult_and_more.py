# Generated by Django 5.0.6 on 2024-06-01 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0003_rename_seasonresults_seasonresult_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonresult',
            name='avgQuali',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='seasonresult',
            name='avgResult',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='seasonresult',
            name='constructorId',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='seasonresult',
            name='driverId',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='trackresult',
            name='avgQuali',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='trackresult',
            name='avgResult',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='trackresult',
            name='constructorId',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='trackresult',
            name='driverId',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='trackresult',
            name='trackId',
            field=models.CharField(default='none', max_length=64),
            preserve_default=False,
        ),
    ]