# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0015_auto_20161119_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='dj',
            field=models.ForeignKey(blank=True, to='djeer_auth.Dj', null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='host',
            field=models.ForeignKey(blank=True, to='djeer_auth.Host', null=True),
        ),
    ]
