# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0022_notification_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='url',
            field=models.CharField(default='', max_length=100, null=True, blank=True),
        ),
    ]
