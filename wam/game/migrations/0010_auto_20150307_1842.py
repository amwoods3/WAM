# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20150307_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastGames',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player1_id', models.PositiveIntegerField()),
                ('player2_id', models.PositiveIntegerField()),
                ('user_ai_title', models.CharField(max_length=100)),
                ('game_history', models.CharField(max_length=300)),
                ('did_player1_win', models.BooleanField(default=True)),
                ('player1_ai_title', models.CharField(max_length=100)),
                ('player2_ai_title', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userstats',
            name='game_history',
        ),
        migrations.RemoveField(
            model_name='userstats',
            name='who_played_against',
        ),
        migrations.AddField(
            model_name='userstats',
            name='user_ai_draws',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
