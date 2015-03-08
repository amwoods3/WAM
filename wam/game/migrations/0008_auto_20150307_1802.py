# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20150305_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.PositiveIntegerField()),
                ('user_ai_title', models.CharField(max_length=100)),
                ('user_ai_wins', models.PositiveIntegerField()),
                ('user_ai_losses', models.PositiveIntegerField()),
                ('game_history', models.CharField(max_length=300)),
                ('who_played_against', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='game',
            name='game_history',
        ),
        migrations.RemoveField(
            model_name='game',
            name='game_name',
        ),
        migrations.AlterField(
            model_name='game',
            name='game_state',
            field=models.CharField(max_length=800),
            preserve_default=True,
        ),
    ]
