# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0006_auto_20161114_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='genre',
            field=models.TextField(null=True, blank=True),
        ),
    ]
