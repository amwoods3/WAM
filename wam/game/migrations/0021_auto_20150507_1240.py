# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_auto_20150507_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastgames',
            name='game_history',
            field=models.CharField(max_length=2000),
            preserve_default=True,
        ),
    ]
