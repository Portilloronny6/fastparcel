# Generated by Django 4.1 on 2022-10-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0006_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='delivery_photo',
            field=models.ImageField(blank=True, null=True, upload_to='jobs/delivery/%d-%m-%Y/'),
        ),
        migrations.AddField(
            model_name='job',
            name='pickedup_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='pickup_photo',
            field=models.ImageField(blank=True, null=True, upload_to='jobs/pickup/%d-%m-%Y/'),
        ),
    ]