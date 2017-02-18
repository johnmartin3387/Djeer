# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0017_auto_20161119_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='value',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
