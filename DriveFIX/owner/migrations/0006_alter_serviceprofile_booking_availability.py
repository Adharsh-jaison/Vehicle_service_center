# Generated by Django 5.1.1 on 2024-10-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0005_remove_serviceprofile_service_center_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprofile',
            name='booking_availability',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
