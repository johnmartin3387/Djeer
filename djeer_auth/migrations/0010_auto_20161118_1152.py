# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0009_bid_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 18, 11, 52, 17, 807558, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 18, 11, 52, 26, 447433, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
