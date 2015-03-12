# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20150307_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pastgames',
            name='user_ai_title',
        ),
    ]
