# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0005_auto_20161114_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='lat',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='lng',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
    ]
