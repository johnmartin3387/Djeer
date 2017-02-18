# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0021_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
