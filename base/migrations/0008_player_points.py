# Generated by Django 3.2 on 2023-01-30 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_player_difference'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
