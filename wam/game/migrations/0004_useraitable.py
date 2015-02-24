# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_userlogin_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAiTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_ai', models.FilePathField(path=b'/scripts', recursive=True, match=b'*.py')),
                ('user_id', models.ForeignKey(to='game.UserLogin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
