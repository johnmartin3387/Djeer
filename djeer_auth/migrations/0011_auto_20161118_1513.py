# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0010_auto_20161118_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='hours',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='price',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
