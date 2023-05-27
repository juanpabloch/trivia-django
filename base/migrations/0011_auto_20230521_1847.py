# Generated by Django 3.2 on 2023-05-21 21:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_rename_user_player_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='category',
        ),
        migrations.RemoveField(
            model_name='player',
            name='difference',
        ),
        migrations.RemoveField(
            model_name='player',
            name='difficulty',
        ),
        migrations.RemoveField(
            model_name='player',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='player',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='player',
            name='user_id',
        ),
        migrations.AddField(
            model_name='player',
            name='active',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='player',
            name='banned',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='country',
            field=models.CharField(default='argentina', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.EmailField(default='juanpablochoter@gmail.com', max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='name',
            field=models.CharField(default='juanpa', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='password',
            field=models.CharField(default='123456jpc', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='q_answered',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='q_correctly',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='q_history',
            field=models.TextField(default='jajaja'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='register',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 5, 21, 21, 47, 56, 400329, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='player',
            name='points',
            field=models.IntegerField(default=1000),
        ),
    ]
