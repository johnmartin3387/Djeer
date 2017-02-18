# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dj',
            name='event_type',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dj',
            name='genre',
            field=models.TextField(null=True, blank=True),
        ),
    ]
