# Generated by Django 5.1.4 on 2025-03-31 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_profile_age_alter_profile_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile_phone',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
