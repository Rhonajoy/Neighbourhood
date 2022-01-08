# Generated by Django 3.2.9 on 2022-01-08 14:34

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neighboor', '0003_remove_location_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
