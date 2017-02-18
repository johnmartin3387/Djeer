# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0019_dj_stripe_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='chat',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
