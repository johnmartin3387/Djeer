# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0018_review_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='dj',
            name='stripe_uid',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
    ]
