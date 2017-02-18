# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0011_auto_20161118_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='message',
            field=models.TextField(default='', null=True, blank=True),
        ),
    ]
