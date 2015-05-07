# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_auto_20150507_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastgames',
            name='game_history',
            field=models.CharField(max_length=5000),
            preserve_default=True,
        ),
    ]
