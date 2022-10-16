# Generated by Django 4.1 on 2022-10-16 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0004_job_delivery_address_job_delivery_lat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='distance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='job',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='job',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
