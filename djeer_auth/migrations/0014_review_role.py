# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0013_auto_20161119_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='role',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
