# Generated by Django 5.1.4 on 2025-05-01 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_announsment_alter_testbalancer_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='micromatch',
            name='team1_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='micromatch',
            name='team2_score',
            field=models.IntegerField(default=0),
        ),
    ]
