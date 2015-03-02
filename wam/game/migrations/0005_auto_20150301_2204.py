# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_useraitable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='player1_name',
        ),
        migrations.RemoveField(
            model_name='game',
            name='player2_name',
        ),
        migrations.AddField(
            model_name='game',
            name='game_history',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='player1_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='player2_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
