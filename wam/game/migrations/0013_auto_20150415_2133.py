# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_useraitable_user_ai_game_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pastgames',
            name='player1_total_time',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pastgames',
            name='player2_total_time',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
