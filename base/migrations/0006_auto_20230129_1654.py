# Generated by Django 3.2 on 2023-01-29 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20230129_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
