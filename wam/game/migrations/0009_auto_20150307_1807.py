# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20150307_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_state', models.CharField(max_length=800)),
                ('last_move', models.CharField(max_length=80)),
                ('player1_id', models.PositiveIntegerField()),
                ('player2_id', models.PositiveIntegerField()),
                ('timer', models.PositiveIntegerField()),
                ('is_player1_turn', models.BooleanField(default=True)),
                ('player1_ai', models.FilePathField(path=b'/scripts', recursive=True, match=b'*.py')),
                ('player2_ai', models.FilePathField(path=b'/scripts', recursive=True, match=b'*.py')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Game',
        ),
    ]
