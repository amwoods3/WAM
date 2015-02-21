# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_name', models.CharField(max_length=100)),
                ('game_state', models.CharField(max_length=200)),
                ('last_move', models.CharField(max_length=80)),
                ('player1_name', models.CharField(max_length=50)),
                ('player2_name', models.CharField(max_length=50)),
                ('timer', models.PositiveIntegerField()),
                ('is_player1_turn', models.BooleanField(default=True)),
                ('player1_ai', models.FilePathField(path=b'/scripts', recursive=True, match=b'*.py')),
                ('player2_ai', models.FilePathField(path=b'/scripts', recursive=True, match=b'*.py')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
