# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0008_bid_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 18, 8, 20, 37, 501410, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
