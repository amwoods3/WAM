# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20150302_0949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraitable',
            name='user_ai',
        ),
        migrations.AddField(
            model_name='useraitable',
            name='user_ai_gen_title',
            field=models.FilePathField(default='', path=b'/scripts', recursive=True, match=b'*.py'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useraitable',
            name='user_ai_title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
