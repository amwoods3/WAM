# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_remove_pastgames_user_ai_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraitable',
            name='user_ai_game_name',
            field=models.CharField(default='tic_tac_toe', max_length=50),
            preserve_default=False,
        ),
    ]
