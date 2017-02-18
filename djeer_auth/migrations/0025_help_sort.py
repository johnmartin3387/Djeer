# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0024_help'),
    ]

    operations = [
        migrations.AddField(
            model_name='help',
            name='sort',
            field=models.IntegerField(default=100, null=True, blank=True),
        ),
    ]
