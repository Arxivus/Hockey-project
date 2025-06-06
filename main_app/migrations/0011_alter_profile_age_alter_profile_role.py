# Generated by Django 5.1.4 on 2025-04-27 18:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_micromatch_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(6), django.core.validators.MaxValueValidator(90)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('S', 'спортсмен'), ('C', 'тренер'), ('R', 'судья')], default='S'),
        ),
    ]
