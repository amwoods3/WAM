# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_auto_20150419_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='activegame',
            name='game_type',
            field=models.CharField(default=b'temp', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pastgames',
            name='game_type',
            field=models.CharField(default=b'temp', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userstats',
            name='game_type',
            field=models.CharField(default=b'temp', max_length=50),
            preserve_default=True,
        ),
    ]
