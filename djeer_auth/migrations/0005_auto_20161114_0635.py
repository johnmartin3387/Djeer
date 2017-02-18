# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0004_auto_20161112_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='lat',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='address',
            name='lng',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
