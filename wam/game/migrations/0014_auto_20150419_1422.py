# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20150415_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activegame',
            name='timer',
        ),
        migrations.AddField(
            model_name='activegame',
            name='player1_timer',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activegame',
            name='player2_timer',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
