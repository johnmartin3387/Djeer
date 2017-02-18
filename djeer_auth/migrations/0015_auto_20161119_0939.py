# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0014_review_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='dj',
            name='score',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='score',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
