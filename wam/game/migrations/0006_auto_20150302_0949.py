# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20150301_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraitable',
            name='user_id',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
    ]
