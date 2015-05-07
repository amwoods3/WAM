# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20150420_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastgames',
            name='game_history',
            field=models.CharField(max_length=100000),
            preserve_default=True,
        ),
    ]
