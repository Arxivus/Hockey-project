# Generated by Django 5.1.4 on 2025-03-30 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
