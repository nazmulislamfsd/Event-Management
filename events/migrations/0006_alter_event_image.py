# Generated by Django 5.2 on 2025-07-04 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, default='Event_images/default.jpg', null=True, upload_to='event_images/'),
        ),
    ]
