# Generated by Django 4.2.7 on 2024-01-27 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Phone', models.BigIntegerField(null=True)),
                ('Qulification', models.CharField(max_length=100)),
                ('Interest', models.CharField(max_length=100)),
                ('Subject', models.CharField(max_length=100, null=True)),
                ('State', models.CharField(max_length=100)),
                ('Country', models.CharField(max_length=100, null=True)),
                ('City', models.CharField(max_length=100, null=True)),
                ('Landmark', models.CharField(max_length=100, null=True)),
                ('DOB', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
