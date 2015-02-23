# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_userlogin'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlogin',
            name='email',
            field=models.CharField(default='example@provider.com', max_length=100),
            preserve_default=False,
        ),
    ]
